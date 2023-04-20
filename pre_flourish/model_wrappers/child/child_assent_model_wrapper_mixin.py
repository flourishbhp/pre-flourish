from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

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
    def assent_model_obj(self):
        """Returns a child assent model instance or None.
        """
        try:
            return self.assent_model_cls.objects.filter(
                **self.assent_options).latest('consent_datetime')
        except ObjectDoesNotExist:
            return None

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
                # create options based on caregiverchildconsent, which is either
                # version 1 or version 2

                wrapped_entries.append(self.assent_model_wrapper_cls(model_obj))
        return wrapped_entries

    @property
    def wrapped_child_assents(self):
        wrapped_assents = []
        for assent in self.child_assents:
            wrapped_assents.append(PreFlourishChildAssentModelWrapper(model_obj=assent))
        return wrapped_assents

    def child_assents_exists(self) -> bool:

        exists_conditions = list()

        if getattr(self, 'consent_model_obj', None):
            caregiverchildconsents = \
                self.consent_model_obj.preflourishcaregiverchildconsent_set \
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
            identities = self.consent_model_obj.preflourishcaregiverchildconsent_set\
                .values_list(
                'identity', flat=True)
            return self.assent_model_cls.objects.filter(identity__in=identities)

    def create_child_assent_options(self, caregiverchildconsent):
        """Returns a dictionary of options to create a new assent model instance."""

        first_name = caregiverchildconsent.first_name
        last_name = caregiverchildconsent.last_name
        initials = self.set_initials(first_name, last_name)

        options = dict(
            subject_identifier=caregiverchildconsent.subject_identifier,
            first_name=first_name,
            last_name=last_name,
            initials=initials,
            gender=caregiverchildconsent.gender,
            identity=caregiverchildconsent.identity,
            identity_type=caregiverchildconsent.identity_type,
            confirm_identity=caregiverchildconsent.confirm_identity,
            dob=caregiverchildconsent.child_dob)
        return options

    @property
    def caregiver_childconsent_cls(self):
        return django_apps.get_model(self.model)

    @property
    def caregiverchildconsent_obj(self):
        """Returns a caregiver child consent model instance or None.
        """
        try:
            # was returning non with caregiverchildconsent_options, so subject identifier
            # and version was used instead
            return self.caregiver_childconsent_cls.objects.get(
                subject_identifier=self.subject_identifier,
            )
        except self.caregiver_childconsent_cls.DoesNotExist:
            return None

    @property
    def heu_participant(self):
        try:
            heu_huu_match_obj = self.heu_huu_match_cls.objects.get(
                huu_prt=self.subject_identifier)
        except self.heu_huu_match_cls.DoesNotExist:
            return None
        else:
            return heu_huu_match_obj.heu_prt

    def set_initials(self, first_name=None, last_name=None):
        initials = ''
        if first_name and last_name:
            if (len(first_name.split(' ')) > 1):
                first = first_name.split(' ')[0]
                middle = first_name.split(' ')[1]
                initials = f'{first[:1]}{middle[:1]}{last_name[:1]}'
            else:
                initials = f'{first_name[:1]}{last_name[:1]}'
        return initials
