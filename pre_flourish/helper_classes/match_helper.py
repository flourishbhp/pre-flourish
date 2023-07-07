from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps


class MatchHelper:
    matrix_pool_model = 'pre_flourish.matrixpool'

    @property
    def matrix_pool_cls(self):
        return django_apps.get_model(self.matrix_pool_model)

    bmi_range_to_group = {
        (00.0, 14.9): '<14.9',
        (15, 17.9): '15-17.9',
        (18, float('inf')): '>18'
    }

    age_range_to_group = [(10, 13), (14, 16), (17, 21)]

    @staticmethod
    def calculate_age(child_dob):
        return relativedelta(datetime.now(), child_dob).years

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
