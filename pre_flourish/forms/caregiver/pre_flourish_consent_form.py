from django import forms
from django.apps import apps as django_apps
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
# from flourish_form_validations.form_validators import SubjectConsentFormValidator
from ...models import PreFlourishConsent
from ...models import PreFlourishSubjectScreening


class PreFlourishConsentForm(SiteModelFormMixin, FormValidatorMixin,
                             forms.ModelForm):

    # form_validator_cls = SubjectConsentFormValidator
    #
    # form_validator_cls.subject_consent_model = 'pre_flourish.preflourishconsent'
    #
    # form_validator_cls.caregiver_locator_model = None
    
    caregiver_locator_model = 'flourish_caregiver.caregiverlocator'
    
    @property
    def caregiver_locator_model_cls(self):
        return django_apps.get_model(self.caregiver_locator_model)
    

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Pre Flourish Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.screening_identifier = self.initial.get('screening_identifier', None)
        
        
        if self.caregiver_locator_model_obj:
            
            if self.caregiver_locator_model_obj.first_name:
                self.initial['first_name'] = self.caregiver_locator_model_obj.first_name
                
            if self.caregiver_locator_model_obj.last_name:
                self.initial['last_name'] = self.caregiver_locator_model_obj.last_name
            
            if self.caregiver_locator_model_obj.first_name and self.caregiver_locator_model_obj.last_name:
                
                first_name = self.caregiver_locator_model_obj.first_name
                last_name = self.caregiver_locator_model_obj.last_name
                
                self.initial['initials'] = f'{first_name[0]}{last_name[0]}'.upper()
        
    @property  
    def caregiver_locator_model_obj(self):
        if self.screening_identifier:
            try:
                screening = PreFlourishSubjectScreening.objects.get(
                    screening_identifier = self.screening_identifier)
                
                locator_obj = self.caregiver_locator_model_cls.objects.get(
                    study_maternal_identifier = screening.previous_subject_identifier
                )
                
            except self.caregiver_locator_model_cls.DoesNotExist:
                pass
            except self.caregiver_locator_model_cls.MultipleObjectsReturned:
                pass
            except PreFlourishSubjectScreening.DoesNotExist:
                pass
            else:
                return locator_obj
            
        
    

    class Meta:
        model = PreFlourishConsent
        fields = '__all__'
