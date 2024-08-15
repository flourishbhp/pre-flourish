from collections import defaultdict

from django.db.models import Max
from edc_constants.constants import MALE
from tqdm import tqdm

from .match_helper import MatchHelper


class HUUPoolGeneration(MatchHelper):

    def __init__(self, subject_identifiers=None):
        self.subject_identifiers = subject_identifiers

    @property
    def breakdown_participants(self):
        if self.subject_identifiers:
            latest_huu_pre_enrollment_ids = self.huu_pre_enrollment_cls.objects.filter(
                pre_flourish_visit__subject_identifier__in=self.subject_identifiers).values(
                    'pre_flourish_visit__subject_identifier').annotate(
                        latest_report_date=Max('report_datetime')).values_list('id', flat=True)

            participants = self.get_valid_participants(latest_huu_pre_enrollment_ids)
            bmi_age_data, _ = self.get_huu_bmi_age_data(participants, active_match=True)
            return bmi_age_data

    def generate_pool(self):
        latest_huu_pre_enrollment_ids = \
            self.huu_pre_enrollment_cls.objects.values(
                'pre_flourish_visit__subject_identifier').annotate(
                latest_report_date=Max('report_datetime')).values_list('id',
                                                                       flat=True)
        participants = self.get_valid_participants(latest_huu_pre_enrollment_ids)
        bmi_age_data, subject_data = self.get_huu_bmi_age_data(participants)
        self.huu_obj_clean_up()
        self.prepare_create_pool('huu', bmi_age_data, subject_data)

    def get_valid_participants(self, latest_huu_pre_enrollment_ids):
        participants = self.huu_pre_enrollment_cls.objects.filter(
            id__in=latest_huu_pre_enrollment_ids,
            child_height__isnull=False,
            child_height__gt=0,
            child_weight_kg__isnull=False,
            child_weight_kg__gt=0,
        )
        return participants

    def huu_obj_clean_up(self):
        self.matrix_pool_cls.objects.filter(pool='huu').delete()

    def get_huu_bmi_age_data(self, participants, active_match=False):
        if not participants:
            return {}, {}
        bmi_age_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        subject_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for participant in tqdm(participants):
            if participant.child_height > 0 and participant.child_weight_kg > 0 and \
                    participant.child_age and participant.gender:
                bmi = participant.child_weight_kg / (
                        (participant.child_height / 100) ** 2)
                bmi_group = self.bmi_group(bmi)
                age_range = self.age_range(participant.child_age)
                if active_match and not age_range and participant.child_age < 9.5:
                    age_range = '(0, 9.5)'
                gender = 'male' if participant.gender == MALE else 'female'
                if bmi_group is None or age_range is None:
                    continue
                bmi_age_data[bmi_group][str(age_range)][gender] += 1
                subj_id = participant.pre_flourish_visit.subject_identifier
                subject_data[bmi_group][str(age_range)][gender].append(subj_id)

        return bmi_age_data, subject_data
