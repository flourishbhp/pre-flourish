from django.apps import apps as django_apps


class FlourishChildConsentModelWrapperMixin:

    @property
    def flourish_child_consent_cls(self):
        return django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

    @property
    def is_flourish_consented(self):
        is_consented = self.flourish_child_consent_cls.objects.filter(
            study_child_identifier=self.subject_identifier).exists()
        return is_consented
