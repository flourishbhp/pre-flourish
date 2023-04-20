from django.apps import apps as django_apps
from edc_base.utils import age, get_utcnow


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

    def __init__(self, dob=None, child_weight_kg=None, child_height_cm=None,
                 subject_identifier=None, gender=None):
        self.subject_identifier = subject_identifier
        self.dob = dob
        self.child_weight_kg = child_weight_kg
        self.child_height_cm = child_height_cm
        self.gender = gender

    @property
    def child_consent_cls(self):
        return django_apps.get_model('flourish_caregiver.caregiverchildconsent')

    @property
    def clinical_measurements_cls(self):
        return django_apps.get_model('flourish_child.childclinicalmeasurements')

    @property
    def huu_pre_enrollment_cls(self):
        return django_apps.get_model('pre_flourish.huuPreEnrollment')

    @property
    def pre_flourish_assents_cls(self):
        return django_apps.get_model('pre_flourish.preflourishchildassent')

    @property
    def flourish_hue_parts(self):
        """Returns a list of all Hiv exposed adolescents who have been consented"""
        child_consents = self.child_consent_cls.objects.all()
        flourish_adolescents = []
        for consent in child_consents:
            if not consent.child_dob:
                continue
            _age = age(consent.child_dob, get_utcnow()).years
            if (_age >= 10 and consent.child_dataset.infant_hiv_exposed in [
                'Exposed', 'exposed'] and
                    consent.subject_identifier != self.subject_identifier and
                    consent.gender == self.gender):
                flourish_adolescents.append(consent)
        return flourish_adolescents

    @property
    def pre_flourish_huu_parts(self):
        pre_flourish_assents = self.pre_flourish_assents_cls.objects.all()
        pre_flourish_adolescents = []
        for assent in pre_flourish_assents:
            if (assent.subject_identifier != self.subject_identifier and
                    assent.gender == self.gender):
                pre_flourish_adolescents.append(assent)
        return pre_flourish_assents

    @property
    def subject_of_interest(self):
        """Returns the subject of interest"""
        subject = self.prepare_subject(self.subject_identifier, self.child_weight_kg,
                                       self.child_height_cm, self.dob)
        return subject

    def prepare_subject(self, subject_identifier, weight_kg, height_cm, dob):
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
        _age = age(dob, get_utcnow()).years
        bmi = float(self.calculate_bmi_adolescents(weight_kg=weight_kg, height=height_cm))

        return {
            'subject_identifier': subject_identifier,
            'age': _age,
            'bmi': bmi
        }

    def find_matching_flourish(self):
        """Finds the first flourish hue part that matches the subject's age and BMI.

        Returns:
            The matching flourish hue part, or None if no match is found.
        """
        for flourish_part in self.flourish_hue_parts:
            try:
                clinical_measurements_obj = self.clinical_measurements_cls.objects.filter(
                    child_visit__subject_identifier=flourish_part.subject_identifier
                ).latest('report_datetime')
            except self.clinical_measurements_cls.DoesNotExist:
                pass
            else:
                prepared_flourish_part = self.prepare_subject(
                    flourish_part.subject_identifier,
                    clinical_measurements_obj.child_weight_kg,
                    clinical_measurements_obj.child_height,
                    flourish_part.child_dob)
                if self.have_matching_age_bmi(subject_1=self.subject_of_interest,
                                              subject_2=prepared_flourish_part):
                    return prepared_flourish_part

        return None

    def find_matching_pre_flourish(self):
        """Finds the first pre flourish huu part that matches the subject's age and BMI.

        Returns:
            The matching pre flourish huu part, or None if no match is found.
        """
        for pre_flourish_part in self.pre_flourish_huu_parts:
            try:
                huu_pre_enrollment_obj = self.huu_pre_enrollment_cls.objects.filter(
                    pre_flourish_visit__subject_identifier=pre_flourish_part
                    .subject_identifier
                ).latest('report_datetime')
            except self.huu_pre_enrollment_cls.DoesNotExist:
                pass
            else:
                prepared_pre_flourish_part = self.prepare_subject(
                    pre_flourish_part.subject_identifier,
                    huu_pre_enrollment_obj.weight,
                    huu_pre_enrollment_obj.height,
                    pre_flourish_part.dob)
                if self.have_matching_age_bmi(subject_1=self.subject_of_interest,
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
        bmi_bins = [(0, 15), (15, 18), (18, float('inf'))]
        if subject_1['bmi'] is None or subject_2['bmi'] is None:
            return False
        subject_1_bmi_bin = next(
            (bmi_bin for bmi_bin in bmi_bins if
             bmi_bin[0] <= subject_1['bmi'] < bmi_bin[1]),
            None)
        subject_2_bmi_bin = next(
            (bmi_bin for bmi_bin in bmi_bins if
             bmi_bin[0] <= subject_2['bmi'] < bmi_bin[1]),
            None)
        if subject_1_bmi_bin is None or subject_2_bmi_bin is None:
            return False
        return subject_1_bmi_bin == subject_2_bmi_bin

    def calculate_bmi_adolescents(self, weight_kg, height):
        height_m = height / 100
        return weight_kg / (height_m ** 2)
