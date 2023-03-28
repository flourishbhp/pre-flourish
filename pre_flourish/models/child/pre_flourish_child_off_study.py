from django.forms import forms

from pre_flourish.action_items import CHILD_OFF_STUDY_ACTION
from pre_flourish.models.caregiver.model_mixins.off_study_mixin import OffStudyMixin
from pre_flourish.models.child.pre_flourish_child_consent import \
    PreFlourishCaregiverChildConsent


class PreFlourishChildOffStudy(OffStudyMixin):
    action_name = CHILD_OFF_STUDY_ACTION

    def get_consent_version(self):
        try:
            consent_obj = PreFlourishCaregiverChildConsent.objects.get(
                subject_identifier=self.subject_identifier)
        except PreFlourishCaregiverChildConsent.DoesNotExist:
            raise forms.ValidationError(
                'Missing Consent Version form. Please complete '
                'it before proceeding.')
        else:
            return consent_obj.version


    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Child Off Study'
        verbose_name_plural = 'Children Off Studies'
