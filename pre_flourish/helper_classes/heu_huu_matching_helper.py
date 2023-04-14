from django.apps import apps as django_apps
from edc_base.utils import age, get_utcnow

import pre_flourish.models.child


class HEUHUUMatchingHelper:
    """Helper class to match HIV exposed adolescents based on age and BMI.

    Attributes:
        subject: A Subject object representing the subject to prepare.

    Methods:
        child_consent_cls: Returns the CaregiverChildConsent model.
        clinical_measurements_cls: Returns the ChildClinicalMeasurements model.
        huu_pre_enrollment_cls: Returns the HUUPreEnrollment model.
        flourish_hue_parts: Returns a list of all HIV-exposed adolescents who have
        been consented.
        prepare_subject: Prepare a dictionary of subject information, including
        their subject
            identifier, age in years, and body mass index (BMI) in kg/m^2,
            using their latest
            available clinical measurements or, if not available, their latest
            available
            pre-enrollment measurements.
        find_match: Finds a match between two HIV-exposed adolescents based on age
        and BMI.
        have_matching_age_bmi: Compare the age and BMI of two subjects.

    Raises:
        None.
    """

    def __init__(self, subject):
        self.subject = subject

    @property
    def child_consent_cls(self):
        return django_apps.get_model('flourish_child.caregiverchildconsent')

    @property
    def clinical_measurements_cls(self):
        return django_apps.get_model('flourish_child.childclinicalmeasurements')

    @property
    def huu_pre_enrollment_cls(self):
        return django_apps.get_model('flourish_child.huuPreEnrollment')

    @property
    def pre_flourish_assents_cls(self):
        return django_apps.get_model(pre_flourish.preflourishchildassent)

    @property
    def flourish_hue_parts(self):
        """Returns a list of all Hiv exposed adolescents who have been consented"""
        child_consents = self.child_consent_cls.objects.all()
        flourish_adolescents = []
        for consent in child_consents:
            if consent.dob >= 14 and consent.child_dataset.infant_hiv_exposedin[
                'Exposed', 'exposed']:
                flourish_adolescents.append(consent)
        return flourish_adolescents

    @property
    def pre_flourish_huu_parts(self):
        return self.pre_flourish_assents_cls.objects.all()

    def prepare_subject(self, subject):
        """Prepare a dictionary of subject information, including their subject
           identifier,
           age in years, and body mass index (BMI) in kg/m^2, using their latest available
           clinical measurements or, if not available, their latest available
           pre-enrollment
           measurements.

           Args:
               subject: A Subject object representing the subject to prepare.

           Returns:
               A dictionary with the following keys:
                   - 'subject_identifier': The subject's identifier.
                   - 'age': The subject's age in years, calculated using their date of
                   birth
                     and the current date/time in UTC.
                   - 'bmi': The subject's BMI in kg/m^2, calculated using their latest
                   available
                     clinical measurements (if available) or, if not available,
                     their latest
                     available pre-enrollment measurements. If BMI cannot be
                     calculated, its value
                     will be set to None.
           """
        clinical_measurements_obj = None
        huu_pre_enrollment_obj = None

        try:
            clinical_measurements_obj = self.clinical_measurements_cls.objects.filter(
                child_visit__subject_identifier=subject.subject_identifier
            ).latest('report_datetime')
        except self.clinical_measurements_cls.DoesNotExist:
            pass

        try:
            huu_pre_enrollment_obj = self.huu_pre_enrollment_cls.objects.filter(
                child_visit__subject_identifier=subject.subject_identifier
            ).latest('report_datetime')
        except self.huu_pre_enrollment_cls.DoesNotExist:
            pass

        bmi = None
        _age = age(subject.dob, get_utcnow())

        if clinical_measurements_obj:
            bmi = self.calculate_bmi_adolescents(
                weight_kg=clinical_measurements_obj.child_weight_kg,
                height=clinical_measurements_obj.child_height)

        if huu_pre_enrollment_obj:
            bmi = self.calculate_bmi_adolescents(
                weight_kg=huu_pre_enrollment_obj.weight,
                height=huu_pre_enrollment_obj.height)

        return {
            'subject_identifier': subject.subject_identifier,
            'age': _age,
            'bmi': bmi
        }

    def find_matching_flourish(self):
        """Finds the first flourish hue part that matches the subject's age and BMI.

        Returns:
            The matching flourish hue part, or None if no match is found.
        """
        subject = self.prepare_subject(self.subject)

        for flourish_part in self.flourish_hue_parts:
            prepared_flourish_part = self.prepare_subject(flourish_part)
            if self.have_matching_age_bmi(subject_1=subject,
                                          subject_2=prepared_flourish_part):
                return prepared_flourish_part

        return None

    def find_matching_pre_flourish(self):
        """Finds the first pre flourish huu part that matches the subject's age and BMI.

        Returns:
            The matching pre flourish huu part, or None if no match is found.
        """
        subject = self.prepare_subject(self.subject)

        for pre_flourish_part in self.pre_flourish_huu_parts:
            prepared_pre_flourish_part = self.prepare_subject(pre_flourish_part)
            if self.have_matching_age_bmi(subject_1=subject,
                                          subject_2=prepared_pre_flourish_part):
                return prepared_pre_flourish_part

        return None

    def have_matching_age_bmi(self, subject_1, subject_2):
        """Compare the age and BMI of two subjects.

       Args:
           subject_1: A dictionary-like object representing the first subject.
           subject_2: A dictionary-like object representing the second subject.

       Returns:
           A boolean value indicating whether the age and BMI of the two subjects match.

       Raises:
           None.
           """
        age_dict = {10: 0, 11: 0, 12: 0, 13: 0, 14: 1, 15: 1, 16: 1, 17: 1, 18: 2, 19: 2,
                    20: 2, 21: 2}
        age_bin = age_dict.get(subject_1['age'], -1)
        if age_bin == -1 or subject_2['age'] not in age_dict:
            return False
        if age_bin != age_dict[subject_2['age']]:
            return False
        bmi_bins = [(0, 15), (15, 18), (18, 21), (21, 25), (25, float('inf'))]
        subject_1_bmi_bin = next(
            (bmi_bin for bmi_bin in bmi_bins if bmi_bin[0] <= subject_1['bmi'] < bmi_bin[1]),
            None)
        subject_2_bmi_bin = next(
            (bmi_bin for bmi_bin in bmi_bins if bmi_bin[0] <= subject_2['bmi'] < bmi_bin[1]),
            None)
        if subject_1_bmi_bin is None or subject_2_bmi_bin is None:
            return False
        return subject_1_bmi_bin == subject_2_bmi_bin

    def calculate_bmi_adolescents(self, weight_kg, height):
        height_m = height / 100
        return weight_kg / (height_m ** 2)
