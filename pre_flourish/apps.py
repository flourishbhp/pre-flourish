from datetime import datetime

from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_visit_tracking.constants import COMPLETED_PROTOCOL_VISIT, LOST_VISIT, \
    MISSED_VISIT, \
    SCHEDULED, UNSCHEDULED


class AppConfig(DjangoAppConfig):
    name = 'pre_flourish'
    verbose_name = 'Pre Flourish'
    admin_site_name = 'pre_flourish_admin'

    consent_version = 4.1
    child_consent_version = 4

    def ready(self):
        import pre_flourish.models.child.signals
        import pre_flourish.models.caregiver.signals


if settings.APP_NAME == 'pre_flourish':
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.constants import COMPLETE_APPT
    from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
    from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
    from edc_timepoint.timepoint import Timepoint
    from edc_timepoint.timepoint_collection import TimepointCollection
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig

    class EdcBaseAppConfig(BaseEdcBaseAppConfig):
        project_name = 'Pre-Flourish'
        institution = 'Botswana-Harvard AIDS Institute'

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='pre_flourish.appointment',
                related_visit_model='pre_flourish.preflourishvisit',
                appt_type='clinic')]

    class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
        timepoints = TimepointCollection(
            timepoints=[
                Timepoint(
                    model='edc_appointment.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='edc_appointment.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
            ])

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'pre_flourish': (
                'pre_flourish_visit', 'pre_flourish.preflourishvisit'), }

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = 'BHP035'
        protocol_name = 'Flourish'
        protocol_number = '035'
        protocol_title = ''
        study_open_datetime = datetime(
            2020, 9, 16, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2023, 12, 31, 23, 59, 59, tzinfo=gettz('UTC'))

    class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
        reason_field = {
            'pre_flourish.preflourishvisit': 'reason',
            'flourish_caregiver.maternalvisit': 'reason',
            'flourish_child.childvisit': 'reason', }
        create_on_reasons = [SCHEDULED, UNSCHEDULED, COMPLETED_PROTOCOL_VISIT]
        delete_on_reasons = [LOST_VISIT, MISSED_VISIT, FAILED_ELIGIBILITY]
