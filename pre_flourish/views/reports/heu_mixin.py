from collections import defaultdict

from django.apps import apps as django_apps
from django.db.models import Max
from edc_constants.constants import MALE

from .report_mixin import ReportsMixin

MALE = 'M'
FEMALE = 'F'


class HEUMixin(ReportsMixin):
    child_clinical_measurements_model = 'flourish_child.childclinicalmeasurements'
    caregiver_child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    bmi_age_data = None

    def __init__(self):
        self.child_clinical_measurements_cls = django_apps.get_model(
            self.child_clinical_measurements_model)
        self.caregiver_child_consent_cls = django_apps.get_model(
            self.caregiver_child_consent_model)

    def get_participants_with_height_weight_dob(self):
        latest_clinical_measurements_ids = \
            self.child_clinical_measurements_cls.objects.values(
                'child_visit__subject_identifier').annotate(
                latest_report_date=Max('report_datetime')).values_list('id',
                                                                       flat=True)

        participants = self.child_clinical_measurements_cls.objects.filter(
            id__in=latest_clinical_measurements_ids,
        ).select_related('child_visit')
        return self.get_heu_bmi_age_data(participants)

    @staticmethod
    def get_age_gender(caregiver_child_consent_cls, participant):
        try:
            consent = caregiver_child_consent_cls.objects.filter(
                subject_identifier=participant.child_visit.subject_identifier
            ).latest('consent_datetime')
        except caregiver_child_consent_cls.DoesNotExist:
            raise ('No consent found for {}'.format(
                participant.child_visit.subject_identifier))
        else:
            return consent.child_dob, consent.gender

    def get_heu_bmi_age_data(self, participants):
        if not participants:
            return {}
        bmi_age_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        subject_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for participant in participants:
            child_dob, gender = self.get_age_gender(self.caregiver_child_consent_cls,
                                                    participant)
            if participant.child_height > 0 and participant.child_weight_kg > 0 and \
                    child_dob and gender:
                _age = self.calculate_age(child_dob)
                _bmi = participant.child_weight_kg / (
                        (participant.child_height / 100) ** 2)

                for bmi_range, bmi_group in self.bmi_range_to_group.items():
                    if bmi_range[0] <= _bmi <= bmi_range[1]:
                        for age_range, age_group in self.age_range_to_group.items():
                            if age_range[0] <= _age < age_range[1]:
                                gender = 'male' if gender == MALE else 'female'
                                bmi_age_data[bmi_group][age_group][gender] += 1
                                subj_id = participant.child_visit.subject_identifier
                                subject_data[bmi_group][age_range][gender].append(subj_id)
                                break
                        break

        return {'bmi_age_data': bmi_age_data, 'subject_data': subject_data}
