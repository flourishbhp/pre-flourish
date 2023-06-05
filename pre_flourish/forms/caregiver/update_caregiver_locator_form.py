from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from edc_action_item import site_action_items
from edc_locator.action_items import SUBJECT_LOCATOR_ACTION

from .form_mixins import SubjectModelFormMixin
from ...models import UpdateCaregiverLocator


class UpdateCaregiverLocatorForm(SubjectModelFormMixin, forms.ModelForm):

    def clean(self):
        self.validate_locator_action_completed()

    def validate_locator_action_completed(self):
        subject_locator_model_cls = django_apps.get_model(
            'flourish_caregiver.caregiverlocator')
        pre_flourish_visit = self.cleaned_data.get('pre_flourish_visit')
        action_cls = site_action_items.get(subject_locator_model_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()
        try:
            action_item_model_cls.objects.get(
                subject_identifier=pre_flourish_visit.subject_identifier,
                action_type__name=SUBJECT_LOCATOR_ACTION)
        except ObjectDoesNotExist:
            raise ValidationError('Please complete the caregiver locator action')

    class Meta:
        model = UpdateCaregiverLocator
        fields = '__all__'
