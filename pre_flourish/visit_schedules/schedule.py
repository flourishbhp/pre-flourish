from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule, Visit

from .crfs import crf
from .requisitions import requisitions

# schedule for new participants
pre_flourish_schedule = Schedule(
    name='pre_flourish_schedule',
    verbose_name='Pre Flourish Schedule',
    onschedule_model='pre_flourish.onschedulepreflourish',
    offschedule_model='pre_flourish.preflourishoffstudy',
    consent_model='pre_flourish.preflourishconsent',
    appointment_model='edc_appointment.appointment')

visit0 = Visit(
    code='1000',
    title='Enrollment Visit',
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions,
    crfs=crf.get(1000),
    facility_name='5-day clinic')

pre_flourish_schedule.add_visit(visit=visit0)
