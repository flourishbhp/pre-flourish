from django.forms import forms
from django.apps import apps as django_apps

from flourish_caregiver.models import CaregiverOffSchedule


class ChildOffSchedule(CaregiverOffSchedule):
    @property
    def latest_consent_obj_version(self):
        child_consent_cls = django_apps.get_model(
            'pre_flourish.preflourishchilddummysubjectconsent')
        subject_consents = child_consent_cls.objects.filter(
            subject_identifier=self.subject_identifier, )
        if subject_consents:
            latest_consent = subject_consents.latest('consent_datetime')
            return latest_consent.version
        else:
            raise forms.ValidationError('Missing Subject Consent form, cannot proceed.')
