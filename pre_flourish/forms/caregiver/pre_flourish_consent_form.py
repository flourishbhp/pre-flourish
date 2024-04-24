from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import FEMALE, YES
from edc_form_validators import FormValidatorMixin
from flourish_caregiver.helper_classes.utils import set_initials

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
        instance = kwargs.get('instance', None)
        previous_instance = getattr(self, 'previous_instance', None)
        self.screening_identifier = initial.get('screening_identifier', None)
        biological_caregiver = getattr(self.screening_obj, 'biological_mother', None)

        initial['biological_caregiver'] = biological_caregiver

        if not instance:
            if (not previous_instance and self.caregiver_locator_model_obj
                    and biological_caregiver == YES):
                first_name = getattr(self.caregiver_locator_model_obj, 'first_name', None)
                last_name = getattr(self.caregiver_locator_model_obj, 'last_name', None)

                initial['first_name'] = first_name
                initial['last_name'] = last_name

                initial['initials'] = set_initials(first_name, last_name)

                initial['gender'] = FEMALE

            if previous_instance:
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
