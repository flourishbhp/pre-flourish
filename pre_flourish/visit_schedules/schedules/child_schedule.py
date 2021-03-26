from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule, Visit

from pre_flourish.visit_schedules.crfs import child_crfs

# schedule for new participants
pre_flourish_child_schedule1 = Schedule(
    name='pre_flourish_child_schedule1',
    verbose_name='Pre Flourish Schedule 1',
    onschedule_model='pre_flourish.onschedulechildpreflourish',
    offschedule_model='pre_flourish.preflourishoffstudy',
    consent_model='pre_flourish.caregiverchildscreeningconsent',
    appointment_model='edc_appointment.appointment')

visit0 = Visit(
    code='1000',
    title='Enrollment Visit',
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=None,
    crfs=child_crfs.get(1000),
    facility_name='5-day clinic')

pre_flourish_child_schedule1.add_visit(visit=visit0)

# schedule for new participants
pre_flourish_child_schedule2 = Schedule(
    name='pre_flourish_child_schedule2',
    verbose_name='Pre Flourish Schedule 2',
    onschedule_model='pre_flourish.onschedulechildpreflourish',
    offschedule_model='pre_flourish.preflourishoffstudy',
    consent_model='pre_flourish.caregiverchildscreeningconsent',
    appointment_model='edc_appointment.appointment')

pre_flourish_child_schedule2.add_visit(visit=visit0)

# schedule for new participants
pre_flourish_child_schedule3 = Schedule(
    name='pre_flourish_child_schedule3',
    verbose_name='Pre Flourish Schedule 3',
    onschedule_model='pre_flourish.onschedulechildpreflourish',
    offschedule_model='pre_flourish.preflourishoffstudy',
    consent_model='pre_flourish.caregiverchildscreeningconsent',
    appointment_model='edc_appointment.appointment')

pre_flourish_child_schedule3.add_visit(visit=visit0)
