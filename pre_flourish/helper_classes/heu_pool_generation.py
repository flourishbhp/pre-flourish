from collections import defaultdict

from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.db.models import OuterRef, Subquery
from edc_base import get_utcnow
from edc_constants.constants import MALE
from tqdm import tqdm

from .match_helper import MatchHelper


class HEUPoolGeneration(MatchHelper):
    child_clinical_measurements_model = 'flourish_child.childclinicalmeasurements'
    caregiver_child_consent_model = 'flourish_caregiver.caregiverchildconsent'
    child_dataset_model = 'flourish_child.childdataset'
    maternal_dataset_model = 'flourish_caregiver.maternaldataset'
    screening_prior_model = 'flourish_caregiver.screeningpriorbhpparticipants'
    child_offstudy_model = 'flourish_prn.childoffstudy'
    bmi_age_data = None

    def __init__(self):
        self.child_clinical_measurements_cls = django_apps.get_model(
            self.child_clinical_measurements_model)
        self.caregiver_child_consent_cls = django_apps.get_model(
            self.caregiver_child_consent_model)
        self.child_dataset_cls = django_apps.get_model(
            self.child_dataset_model)
        self.maternal_dataset_cls = django_apps.get_model(
            self.maternal_dataset_model)
        self.screening_prior_model_cls = django_apps.get_model(
            self.screening_prior_model)
        self.child_offstudy_model_cls = django_apps.get_model(
            self.child_offstudy_model)

    def generate_pool(self):
        latest_measurements = self.child_clinical_measurements_cls.objects.filter(
            child_visit__subject_identifier=OuterRef(
                'child_visit__subject_identifier')).order_by(
                    '-report_datetime').values('id')[:1]

        participants = self.child_clinical_measurements_cls.objects.filter(
            id=Subquery(latest_measurements), ).select_related('child_visit')

        return self.get_heu_bmi_age_data(participants)

    def child_consent(self, caregiver_child_consent_cls, participant):
        age_limit = get_utcnow() - relativedelta(years=9, months=6)
        try:
            return caregiver_child_consent_cls.objects.filter(
                subject_identifier=participant.child_visit.subject_identifier,
                child_dob__lte=age_limit,
                study_child_identifier__in=self.exposed_participants
            ).latest('consent_datetime')
        except caregiver_child_consent_cls.DoesNotExist:
            pass

    def check_offstudy(self, participant):
        offstudy = self.child_offstudy_model_cls.objects.filter(
            subject_identifier=participant.child_visit.subject_identifier)
        return offstudy.exists()

    def get_heu_bmi_age_data(self, participants):
        if not participants:
            return {}, {}
        bmi_age_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        subject_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for participant in tqdm(participants):
            child_consent = self.child_consent(self.caregiver_child_consent_cls,
                                               participant)
            child_offstudy = self.check_offstudy(participant)
            if not child_consent or child_offstudy:
                continue
            child_dob = child_consent.child_dob
            gender = child_consent.gender
            if participant.child_height > 0 and participant.child_weight_kg > 0 and \
                    child_dob and gender:
                _age = self.calculate_age(child_dob)
                _bmi = participant.child_weight_kg / (
                        (participant.child_height / 100) ** 2)
                gender = 'male' if gender == MALE else 'female'
                bmi_group = self.bmi_group(_bmi)
                age_range = self.age_range(_age)
                if bmi_group is None or age_range is None:
                    continue
                bmi_age_data[bmi_group][age_range][gender] += 1
                subj_id = participant.child_visit.subject_identifier
                subject_data[bmi_group][age_range][gender].append(subj_id)

        self.prepare_create_pool('heu', bmi_age_data, subject_data)

    @property
    def exposed_participants(self):
        return self.child_dataset_cls.objects.filter(
            infant_hiv_exposed__in=['Exposed', 'exposed']).values_list(
            'study_child_identifier', flat=True)
