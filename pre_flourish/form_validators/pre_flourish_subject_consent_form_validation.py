import re
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import relativedelta
from edc_constants.constants import FEMALE, MALE, NO, YES, NOT_APPLICABLE
from edc_form_validators import FormValidator
from flourish_form_validations.form_validators import SubjectConsentFormValidator


class PreFlourishConsentFormValidator(SubjectConsentFormValidator):
    subject_consent_model = 'pre_flourish.preflourishconsent'
    pre_flourish_screening_model = 'pre_flourish.preflourishsubjectscreening'

    def clean(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get('subject_identifier')
        self.screening_identifier = cleaned_data.get('screening_identifier')
        super().clean()

        self.clean_full_name_syntax()
        self.clean_initials_with_full_name()
        self.validate_recruit_source()
        self.validate_recruitment_clinic()
        self.validate_is_literate()
        self.validate_dob(cleaned_data=self.cleaned_data)
        self.validate_identity_number(cleaned_data=self.cleaned_data)
        self.validate_breastfeed_intent()
        self.validate_child_consent()
        self.validate_birth_date()

    @property
    def pre_flourish_screening_cls(self):
        return django_apps.get_model(self.pre_flourish_screening_model)

    @property
    def pre_flourish_screening(self):

        try:
            pre_flourish_screening = self.pre_flourish_screening_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.pre_flourish_screening.DoesNotExist:
            return None
        else:
            return pre_flourish_screening


    def clean_full_name_syntax(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and not re.match(r'^[A-Z]+$|^([A-Z]+[ ][A-Z]+)$', first_name):
            message = {'first_name': 'Ensure first name is letters (A-Z) in '
                                     'upper case, no special characters, except spaces. Maximum 2 first '
                                     'names allowed.'}
            self._errors.update(message)
            raise ValidationError(message)

        if last_name and not re.match(r'^[A-Z-]+$', last_name):
            message = {'last_name': 'Ensure last name is letters (A-Z) in '
                                    'upper case, no special characters, except hyphens.'}
            self._errors.update(message)
            raise ValidationError(message)

        if first_name and first_name != first_name.upper():
            message = {'first_name': 'First name must be in CAPS.'}
            self._errors.update(message)
            raise ValidationError(message)
        if last_name and last_name != last_name.upper():
            message = {'last_name': 'Last name must be in CAPS.'}
            self._errors.update(message)
            raise ValidationError(message)

    def clean_initials_with_full_name(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        initials = cleaned_data.get("initials")
        try:
            middle_name = None
            is_first_name = False
            new_first_name = None
            if first_name and len(first_name.split(' ')) > 1:
                new_first_name = first_name.split(' ')[0]
                middle_name = first_name.split(' ')[1]

            if middle_name and (middle_name and
                                (initials[:1] != new_first_name[:1] or
                                 initials[1:2] != middle_name[:1])):
                is_first_name = True

            elif not middle_name and initials[:1] != first_name[:1]:
                is_first_name = True

            if is_first_name or initials[-1:] != last_name[:1]:
                raise forms.ValidationError(
                    {'initials': 'Initials do not match full name.'},
                    params={
                        'initials': initials,
                        'first_name': first_name,
                        'last_name': last_name},
                    code='invalid')
        except (IndexError, TypeError):
            raise forms.ValidationError('Initials do not match fullname.')

    def validate_dob(self, cleaned_data=None):
        consent_datetime = cleaned_data.get('consent_datetime')

        if cleaned_data.get('dob') and consent_datetime:
            consent_age = relativedelta(
                consent_datetime.date(), cleaned_data.get('dob')).years
            if consent_age and consent_age < 18:
                message = {'dob':
                               'Participant is less than 18 years, age derived '
                               f'from the DOB is {consent_age}.'}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_child_consent(self):
        cleaned_data = self.cleaned_data
        subject_eligible = self.subject_eligible(cleaned_data=cleaned_data)
        if not subject_eligible and cleaned_data.get('child_consent') != NOT_APPLICABLE:
            message = {'child_consent':
                           'Caregiver is not eligible for participation, this field '
                           'is not applicable.'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_reconsent(self):
        pass

    def validate_birth_date(self):
        consent_datetime = self.cleaned_data.get('consent_datetime')
        consent_age = relativedelta(
            consent_datetime.date(), self.cleaned_data.get('dob')).years
        if self.pre_flourish_screening:
            screening_age = self.pre_flourish_screening.caregiver_age
            if screening_age and consent_age:
                if screening_age != consent_age:
                    message = {'dob':
                                   'Date of birth does not match the age given on the screening form.'}
                    self._errors.update(message)
                    raise ValidationError(message)

