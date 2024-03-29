from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import FEMALE, YES
from edc_form_validators import FormValidatorMixin

from pre_flourish.form_validators import PreFlourishConsentFormValidator
from ...models import PreFlourishConsent
from ...models import PreFlourishSubjectScreening


class PreFlourishConsentForm(SiteModelFormMixin, FormValidatorMixin,
                             forms.ModelForm):
    form_validator_cls = PreFlourishConsentFormValidator
    caregiver_locator_model = 'flourish_caregiver.caregiverlocator'
    screening_model = 'pre_flourish.preflourishsubjectscreening'

    @property
    def caregiver_locator_model_cls(self):
        return django_apps.get_model(self.caregiver_locator_model)

    @property
    def screening_model_cls(self):
        return django_apps.get_model(self.screening_model)

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Pre Flourish Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = getattr(self, 'instance', None)
        self.screening_identifier = initial.get('screening_identifier', None)
        biological_caregiver = getattr(self.screening_obj, 'biological_mother', None)

        if self.caregiver_locator_model_obj and biological_caregiver == YES:

            if self.caregiver_locator_model_obj.first_name:
                initial['first_name'] = self.caregiver_locator_model_obj.first_name

            if self.caregiver_locator_model_obj.last_name:
                initial['last_name'] = self.caregiver_locator_model_obj.last_name

            if self.caregiver_locator_model_obj.first_name and \
                    self.caregiver_locator_model_obj.last_name:
                first_name = self.caregiver_locator_model_obj.first_name
                last_name = self.caregiver_locator_model_obj.last_name
                initial['initials'] = f'{first_name[0]}{last_name[0]}'.upper()

            initial['gender'] = FEMALE

        initial['biological_caregiver'] = biological_caregiver
        previous_instance = getattr(self, 'previous_instance', None)
        if not instance and previous_instance:
            for key in self.base_fields.keys():
                initial[key] = previous_instance[0].get(key, None)
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    @property
    def caregiver_locator_model_obj(self):
        if self.screening_identifier:
            try:
                screening = PreFlourishSubjectScreening.objects.get(
                    screening_identifier=self.screening_identifier)

                locator_obj = self.caregiver_locator_model_cls.objects.get(
                    study_maternal_identifier=screening.study_maternal_identifier
                )

            except self.caregiver_locator_model_cls.DoesNotExist:
                pass
            except self.caregiver_locator_model_cls.MultipleObjectsReturned:
                pass
            except PreFlourishSubjectScreening.DoesNotExist:
                pass
            else:
                return locator_obj

    @property
    def screening_obj(self):
        if self.screening_identifier:
            try:
                return self.screening_model_cls.objects.get(
                    screening_identifier=self.screening_identifier
                )
            except self.screening_model_cls.DoesNotExist:
                raise

    def has_changed(self):
        return True

    def clean(self):
        """
        Raise ValidationError if least one child consent inline form is not added.
        """
        clean_data = super().clean()

        child_consent_inlines = int(
            self.data.get('preflourishcaregiverchildconsent_set-TOTAL_FORMS', 0))

        if child_consent_inlines == 0:
            raise ValidationError('You must add at least one child consent')
        return clean_data

    class Meta:
        model = PreFlourishConsent
        fields = '__all__'
