from datetime import datetime

from dateutil.relativedelta import relativedelta


class ReportsMixin:
    bmi_range_to_group = {
        (00.0, 14.9): '<14.9',
        (15, 17.9): '15-17.9',
        (18, float('inf')): '>18'
    }

    age_range_to_group = {
        (10, 13): 'age_group_1',
        (14, 16): 'age_group_2',
        (17, 21): 'age_group_3'
    }

    @staticmethod
    def calculate_age(child_dob):
        return relativedelta(datetime.now(), child_dob).years
