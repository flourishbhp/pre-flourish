from datetime import datetime

from dateutil.relativedelta import relativedelta


class ReportsMixin:
    bmi_groups = [
        {'name': '<14.9', 'min': 00.0, 'max': 14.9},
        {'name': '15-17.9', 'min': 15, 'max': 17.9},
        {'name': '>18', 'min': 18, 'max': float('inf')}
    ]
    age_groups = [
        {'name': 'age_group_1', 'min': 10, 'max': 13},
        {'name': 'age_group_2', 'min': 14, 'max': 16},
        {'name': 'age_group_3', 'min': 17, 'max': 21}
    ]

    @staticmethod
    def calculate_age(child_dob):
        return relativedelta(datetime.now(), child_dob).years
