from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from edc_base import get_utcnow
from edc_identifier.infant_identifier import InfantIdentifier as BaseInfantIdentifier, \
    InfantIdentifierError
from edc_identifier.subject_identifier import SubjectIdentifier as \
    BaseSubjectIdentifier

edc_device_app_config = django_apps.get_app_config('edc_device')
edc_protocol_app_config = django_apps.get_app_config('edc_protocol')


class SubjectIdentifier(BaseSubjectIdentifier):
    template = '{protocol_number}-0{site_id}{device_id}{sequence}'

    def __init__(self, caregiver_type=None, **kwargs):
        self.caregiver_type = caregiver_type
        super().__init__(**kwargs)

    @property
    def identifier(self):
        """Returns a new and unique identifier and updates
        the IdentifierModel.
        """
        if not self._identifier:
            self.pre_identifier()
            self._identifier = self.template.format(**self.template_opts)
            check_digit = self.checkdigit.calculate_checkdigit(
                ''.join(self._identifier.split('-')))
            if self.caregiver_type:
                self._identifier = f'{self.caregiver_type}{self._identifier}-' \
                                   f'{check_digit}P'
            self.identifier_model = self.identifier_model_cls.objects.create(
                name=self.label,
                sequence_number=self.sequence_number,
                identifier=self._identifier,
                protocol_number=self.protocol_number,
                device_id=self.device_id,
                model=self.requesting_model,
                site=self.site,
                identifier_type=self.identifier_type)
            self.post_identifier()
        return self._identifier

    def post_identifier(self):
        model = django_apps.get_model('pre_flourish.preflourishregisteredsubject')
        model.objects.create(
            subject_identifier=self.identifier,
            site=self.site,
            subject_type=self.identifier_type,
            last_name=self.last_name,
            registration_datetime=get_utcnow())


class PreFlourishIdentifier(BaseSubjectIdentifier):
    template = 'PF{protocol_number}-0{site_id}{device_id}{sequence}'


class PFInfantIdentifier(BaseInfantIdentifier):

    def __init__(self, maternal_identifier=None, requesting_model=None,
                 birth_order=None, live_infants=None, template=None,
                 first_name=None, initials=None, last_name=None, registration_status=None,
                 registration_datetime=None, subject_type=None,
                 supplied_infant_suffix=None):
        self.supplied_infant_suffix = supplied_infant_suffix
        self._first_name = first_name
        self._identifier = None
        self._infant_suffix = None
        # check maternal identifier
        rs = self.verify_maternal_identifier(maternal_identifier)
        self.last_name = last_name or rs.last_name
        self.maternal_identifier = maternal_identifier
        self.birth_order = birth_order
        self.initials = initials
        self.live_infants = live_infants
        self.registration_datetime = registration_datetime or get_utcnow()
        self.registration_status = registration_status or 'DELIVERED'
        self.requesting_model = requesting_model
        self.subject_type = subject_type or self.subject_type
        self.template = template or self.template
        self.identifier

    @property
    def registration_model(self):
        return django_apps.get_model('pre_flourish.preflourishregisteredsubject')

    def verify_maternal_identifier(self, maternal_identifier):
        try:
            return self.registration_model.objects.get(
                subject_identifier=maternal_identifier)
        except ObjectDoesNotExist:
            raise InfantIdentifierError(
                f'Failed to create infant identifier. Invalid maternal '
                f'identifier. Got {maternal_identifier}')

    @property
    def identifier(self):
        if not self._identifier:
            identifier = self.template.format(
                maternal_identifier=self.maternal_identifier,
                infant_suffix=self.infant_suffix)
            try:
                self.identifier_model_cls.objects.get(identifier=identifier)
            except ObjectDoesNotExist:
                pass
            else:
                raise InfantIdentifierError(
                    f'Infant identifier unexpectedly exists. '
                    f'See model {self.identifier_model_cls._meta.label_lower}. '
                    f'Got {identifier}')
            try:
                self.registration_model.objects.get(subject_identifier=identifier)
            except ObjectDoesNotExist:
                pass
            else:
                raise InfantIdentifierError(
                    f'Infant identifier unexpectedly exists. '
                    f'See {self.registration_model._meta.label_lower}. '
                    f'Got {identifier}')
            # update identifier model
            self.identifier_model_cls.objects.create(
                name=self.label,
                sequence_number=self.infant_suffix,
                identifier=identifier,
                linked_identifier=self.maternal_identifier,
                protocol_number=edc_protocol_app_config.protocol_number,
                device_id=edc_device_app_config.device_id,
                model=self.requesting_model,
                site=Site.objects.get_current(),
                identifier_type=self.subject_type)
            # update RegisteredSubject
            self.registration_model.objects.create(
                subject_identifier=identifier,
                subject_type=self.subject_type,
                site=Site.objects.get_current(),
                relative_identifier=self.maternal_identifier,
                first_name=self.first_name,
                initials=self.initials,
                registration_status=self.registration_status,
                registration_datetime=self.registration_datetime)
            self._identifier = identifier
        return self._identifier

    @property
    def infant_suffix(self):
        return self.supplied_infant_suffix
