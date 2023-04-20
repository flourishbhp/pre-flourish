from datetime import timedelta
from django.conf import settings
from edc_model_wrapper import ModelWrapper
from edc_base.utils import get_utcnow
from dateutil.relativedelta import relativedelta
from .child_assent_model_wrapper import \
    PreFlourishChildAssentModelWrapper as AssentModelWrapper
from ...models import PreFlourishChildAssent as Assent


class PreFlourishSubjectConsentModelWrapper(ModelWrapper):
    model = 'pre_flourish.preflourishconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']

    @property
    def wrapped_child_assents(self):
        wrapped_assents = []
        for assent in self.child_assents:
            wrapped_assents.append(AssentModelWrapper(model_obj=assent))
        return wrapped_assents

    @property
    def child_assents_exists(self):
        subject_identifiers = self.children_consent_objs.values_list('subject_identifier',
                                                                     flat=True)

        assents_exist = Assent.objects.filter(
            subject_identifier__in=subject_identifiers).exists()

        return assents_exist

    @property
    def child_assents(self):
        assents = []

        least_expected_dob = (get_utcnow() - relativedelta(years=7)).date()

        children_consents = self.children_consent_objs.filter(
            child_dob__lte=least_expected_dob)

        for consent in children_consents:
            try:
                assent = Assent.objects.get(
                    subject_identifier=consent.subject_identifier
                )

            except Assent.DoesNotExist:

                assent = Assent(
                    **self.create_child_assent_options(consent)

                )
                assents.append(assent)
            else:
                assents.append(assent)

        return assents

    @property
    def children_consent_objs(self):
        children_consents = self.object.preflourishcaregiverchildconsent_set.all()
        return children_consents

    def create_child_assent_options(self, caregiverchildconsent):

        options = dict(
            subject_identifier=caregiverchildconsent.subject_identifier,
            first_name=caregiverchildconsent.first_name,
            last_name=caregiverchildconsent.last_name,
            initials=caregiverchildconsent.initials,
            gender=caregiverchildconsent.gender,
            identity=caregiverchildconsent.identity,
            identity_type=caregiverchildconsent.identity_type,
            confirm_identity=caregiverchildconsent.confirm_identity,
            dob=caregiverchildconsent.child_dob)
        return options