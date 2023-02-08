from django.apps import apps as django_apps

from flourish_child.models import ChildAssent
from flourish_dashboard.model_wrappers.child_assent_model_wrapper_mixin import \
    ChildAssentModelWrapperMixin as BaseFlourishChildAssentModelWrapperMixin
from pre_flourish.model_wrappers.caregiver.child_assent_model_wrapper import \
    PreFlourishChildAssentModelWrapper


class ChildAssentModelWrapperMixin(BaseFlourishChildAssentModelWrapperMixin):
    assent_model_wrapper_cls = PreFlourishChildAssentModelWrapper

    @property
    def assent_model_cls(self):
        return django_apps.get_model('pre_flourish.preflourishchildassent')

    @property
    def consent_version_cls(self):
        pass

    @property
    def subject_consent_cls(self):
        return django_apps.get_model('pre_flourish.preflourishconsent')

    @property
    def child_assent(self):
        """"Returns a wrapped saved or unsaved child assent
        """
        if self.child_age >= 7:
            model_obj = self.assent_model_obj or self.assent_model_cls(
                **self.create_child_assent_options(self.caregiverchildconsent_obj))

            return self.assent_model_wrapper_cls(model_obj=model_obj)

    @property
    def child_assents(self):
        wrapped_entries = []
        if getattr(self, 'consent_model_obj', None):
            # set was used, to get care giver child consent in v1 or v2
            caregiverchildconsents = self.consent_model_obj.caregiverchildconsent_set \
                .only('child_age_at_enrollment', 'is_eligible') \
                .filter(is_eligible=True, child_age_at_enrollment__gte=7)

            for caregiverchildconsent in caregiverchildconsents:
                model_obj = self.child_assent_model_obj(caregiverchildconsent) or \
                            self.assent_model_cls(
                                **self.create_child_assent_options(caregiverchildconsent))
                # create options based on caregiverchildconsent, which is either version 1 or version 2

                wrapped_entries.append(self.assent_model_wrapper_cls(model_obj))
        return wrapped_entries

    def child_assents_exists(self) -> bool:

        exists_conditions = list()

        if getattr(self, 'consent_model_obj', None):
            caregiverchildconsents = self.consent_model_obj.preflourishcaregiverchildconsent_set \
                .only('child_age_at_enrollment', 'is_eligible') \
                .filter(is_eligible=True,
                        child_age_at_enrollment__gte=7,
                        child_age_at_enrollment__lt=18)

            for caregiver_childconsent in caregiverchildconsents:
                model_objs = ChildAssent.objects.filter(
                    subject_identifier=caregiver_childconsent.subject_identifier).exists()
                exists_conditions.append(model_objs)

            return all(exists_conditions)

    @property
    def child_assents_qs(self):
        if getattr(self, 'consent_model_obj', None):
            identities = self.consent_model_obj.preflourishcaregiverchildconsent_set.values_list(
                'identity', flat=True)
            return self.assent_model_cls.objects.filter(identity__in=identities)
