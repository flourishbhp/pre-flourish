from collections import defaultdict

from django.apps import apps as django_apps
from django.db.models import Max

from .report_mixin import ReportsMixin

MALE = 'M'
FEMALE = 'F'


class HUUMixin(ReportsMixin):
    huu_pre_enrollment_model = 'pre_flourish.huupreenrollment'

    @property
    def huu_pre_enrollment_cls(self):
        return django_apps.get_model(self.huu_pre_enrollment_model)

    def get_huu_report(self):
        latest_huu_pre_enrollment_ids = \
            self.huu_pre_enrollment_cls.objects.values(
                'pre_flourish_visit__subject_identifier').annotate(
                latest_report_date=Max('report_datetime')).values_list('id',
                                                                       flat=True)
        participants = self.huu_pre_enrollment_cls.objects.filter(
            id__in=latest_huu_pre_enrollment_ids,
            height__isnull=False,
            height__gt=0,
            weight__isnull=False,
            weight__gt=0,
        )
        return self.get_huu_bmi_age_data(participants)

    def get_huu_bmi_age_data(self, participants):
        if not participants:
            return {}
        bmi_range_to_group = {
            ((group := self.bmi_groups[i])['min'], group['max']): group['name'] for i in
            range(len(self.bmi_groups))}
        age_range_to_group = {
            ((group := self.age_groups[i])['min'], group['max']): group['name'] for i in
            range(len(self.age_groups))}
        bmi_age_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        subject_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for participant in participants:
            if participant.child_height > 0 and participant.child_weight_kg > 0 and \
                    participant.child_age and participant.sex:
                bmi = participant.child_weight_kg / (
                        (participant.child_height / 100) ** 2)

                for bmi_range, bmi_group in bmi_range_to_group.items():
                    if bmi_range[0] <= bmi <= bmi_range[1]:
                        for age_range, age_group in age_range_to_group.items():
                            if age_range[0] <= participant.child_age <= age_range[1]:
                                gender = 'male' if participant.sex == MALE else 'female'
                                bmi_age_data[bmi_group][age_group][gender] += 1
                                subj_id = \
                                    participant.pre_flourish_visit.subject_identifier
                                subject_data[bmi_group][age_range][gender].append(subj_id)
                                break
                        break

        return {'bmi_age_data': bmi_age_data, 'subject_data': subject_data}
