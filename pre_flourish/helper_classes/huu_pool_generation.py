from collections import defaultdict

from django.apps import apps as django_apps
from django.db.models import Max
from tqdm import tqdm

from .match_helper import MatchHelper

MALE = 'M'
FEMALE = 'F'


class HUUPoolGeneration(MatchHelper):
    huu_pre_enrollment_model = 'pre_flourish.huupreenrollment'

    @property
    def huu_pre_enrollment_cls(self):
        return django_apps.get_model(self.huu_pre_enrollment_model)

    def generate_pool(self):
        latest_huu_pre_enrollment_ids = \
            self.huu_pre_enrollment_cls.objects.values(
                'pre_flourish_visit__subject_identifier').annotate(
                latest_report_date=Max('report_datetime')).values_list('id',
                                                                       flat=True)
        participants = self.huu_pre_enrollment_cls.objects.filter(
            id__in=latest_huu_pre_enrollment_ids,
            child_height__isnull=False,
            child_height__gt=0,
            child_weight_kg__isnull=False,
            child_weight_kg__gt=0,
        )
        return self.get_huu_bmi_age_data(participants)

    def get_huu_bmi_age_data(self, participants):
        if not participants:
            return {}
        bmi_age_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        subject_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for participant in tqdm(participants):
            if participant.child_height > 0 and participant.child_weight_kg > 0 and \
                    participant.child_age and participant.gender:
                bmi = participant.child_weight_kg / (
                        (participant.child_height / 100) ** 2)
                bmi_group = self.bmi_group(bmi)
                age_range = self.age_range(participant.child_age)
                gender = 'male' if participant.gender == MALE else 'female'
                if bmi_group is None or age_range is None:
                    continue
                bmi_age_data[bmi_group][age_range][gender] += 1
                subj_id = participant.pre_flourish_visit.subject_identifier
                subject_data[bmi_group][age_range][gender].append(subj_id)

        self.prepare_create_pool('huu', bmi_age_data, subject_data)
