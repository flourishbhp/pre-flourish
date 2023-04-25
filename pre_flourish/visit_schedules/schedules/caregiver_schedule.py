from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule, Visit

from pre_flourish.visit_schedules.crfs import caregiver_crfs_1000

# schedule for new participants
pre_flourish_schedule1 = Schedule(
    name='pre_flourish_schedule1',
    verbose_name='Pre Flourish Schedule 1',
    onschedule_model='pre_flourish.onschedulepreflourish',
    offschedule_model='pre_flourish.caregiveroffschedule',
    consent_model='pre_flourish.preflourishconsent',
    appointment_model='pre_flourish.appointment')

visit0 = Visit(
    code='1000',
    title='Enrollment Visit',
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=None,
    crfs=caregiver_crfs_1000,
    facility_name='5-day clinic')

pre_flourish_schedule1.add_visit(visit=visit0)

# schedule for new participants
pre_flourish_schedule2 = Schedule(
    name='pre_flourish_schedule2',
    verbose_name='Pre Flourish Schedule 2',
    onschedule_model='pre_flourish.onschedulepreflourish',
    offschedule_model='pre_flourish.caregiveroffschedule',
    consent_model='pre_flourish.preflourishconsent',
    appointment_model='pre_flourish.appointment')

pre_flourish_schedule2.add_visit(visit=visit0)

# schedule for new participants
pre_flourish_schedule3 = Schedule(
    name='pre_flourish_schedule3',
    verbose_name='Pre Flourish Schedule 3',
    onschedule_model='pre_flourish.onschedulepreflourish',
    offschedule_model='pre_flourish.caregiveroffschedule',
    consent_model='pre_flourish.preflourishconsent',
    appointment_model='pre_flourish.appointment')

pre_flourish_schedule3.add_visit(visit=visit0)
