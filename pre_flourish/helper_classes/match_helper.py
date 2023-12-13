from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from edc_base import get_utcnow


def create_reminder(title, start_date, end_date, remainder_time, note, color='yellow',
                    repeat='once'):
    reminder_cls = django_apps.get_model('flourish_calendar.reminder')
    reminder = reminder_cls.objects.create(title=title,
                                           start_date=start_date,
                                           end_date=end_date,
                                           remainder_time=remainder_time, note=note,
                                           color=color, repeat=repeat)
    reminder.save()
    return reminder


class MatchHelper:
    matrix_pool_model = 'pre_flourish.matrixpool'
    huu_pre_enrollment_model = 'pre_flourish.huupreenrollment'

    @property
    def huu_pre_enrollment_cls(self):
        return django_apps.get_model(self.huu_pre_enrollment_model)

    @property
    def matrix_pool_cls(self):
        return django_apps.get_model(self.matrix_pool_model)

    bmi_range_to_group = {
        (00.0, 14.9): '<14.9',
        (15, 17.9): '15-17.9',
        (18, float('inf')): '>18'
    }

    age_range_to_group = [(9.5, 13), (14, 16), (17, 21)]

    @staticmethod
    def calculate_age(child_dob):
        return relativedelta(datetime.now(), child_dob).years + \
            (relativedelta(datetime.now(), child_dob).months / 12)

    def create_matrix_pool(self, name, bmi_group, gender_group, age_group, count,
                           subject_identifiers):
        defaults = {
            'count': count,
        }
        obj, _ = self.matrix_pool_cls.objects.update_or_create(
            pool=name, bmi_group=bmi_group, age_group=age_group,
            gender_group=gender_group, defaults=defaults
        )
        obj.set_subject_identifiers(subject_identifiers)
        obj.save()

    def prepare_create_pool(self, name, bmi_age_data, subject_data):
        for bmi_group, age_data in bmi_age_data.items():
            for age_group, gender_data in age_data.items():
                for gender_group, count in gender_data.items():
                    subject_identifiers = subject_data[bmi_group][age_group][gender_group]
                    self.create_matrix_pool(
                        name=name, age_group=age_group,
                        bmi_group=bmi_group, gender_group=gender_group,
                        count=count, subject_identifiers=subject_identifiers)

    def bmi_group(self, bmi):
        if bmi is None:
            return None
        for bmi_range, bmi_group in self.bmi_range_to_group.items():
            if bmi_range[0] <= bmi <= bmi_range[1]:
                return bmi_group
        return None

    def age_range(self, age):
        if age is None:
            return None
        for age_range in self.age_range_to_group:
            if age_range[0] <= age < age_range[1]:
                return age_range
        return None

    def heu_huu_match_clean_up(self, subject_identifier):
        matrix_pools = self.matrix_pool_cls.objects.filter(pool='heu')
        for matrix_pool in matrix_pools:
            subject_identifiers, is_changed = self.remove_subject_identifier(
                subject_identifier, matrix_pool.get_subject_identifiers)
            if is_changed:
                matrix_pool.set_subject_identifiers(subject_identifiers)
                matrix_pool.count = matrix_pool.count - 1
                matrix_pool.save()

    def remove_subject_identifier(self, subject_identifier, get_subject_identifiers):
        subject_identifiers = get_subject_identifiers
        if subject_identifier in subject_identifiers:
            index_to_remove = subject_identifiers.index(subject_identifier)
            del subject_identifiers[index_to_remove]
            return subject_identifiers, True

        return subject_identifiers, False

    def create_new_matrix_pool(self, pool, bmi_group, age_group, gender_group,
                               subject_identifier):

        self.heu_huu_match_clean_up(subject_identifier)
        matrix_pool = self.matrix_pool_cls.objects.create(
            pool=pool, bmi_group=bmi_group, age_group=age_group,
            gender_group=gender_group, count=1)
        matrix_pool.set_subject_identifiers([subject_identifier])
        matrix_pool.save()

    def send_email_to_pre_flourish_users(self, huu_matrix_group):
        pre_flourish_group = Group.objects.get(name='pre_flourish')
        pre_flourish_users = pre_flourish_group.user_set.all()

        subject = 'Reminder: Enroll into Flourish'
        subject_identifiers = '\n'.join(
            [matrix.subject_identifiers for matrix in huu_matrix_group])
        subject_identifiers = subject_identifiers.strip('""')

        message = f'This serves as a reminder that these participants are now eligible ' \
                  f'to ' \
                  f'enroll to the flourish edc. Please enroll them! \n\n' \
                  f'Subject Identifier(s):\n' \
                  f'{subject_identifiers}\n'

        recipients = [user.email for user in pre_flourish_users]
        create_reminder(title=subject, start_date=get_utcnow().date(),
                        end_date=get_utcnow().date(),
                        remainder_time=get_utcnow().time(),
                        note=message, )
        send_mail(subject=subject, message=message,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=recipients)
