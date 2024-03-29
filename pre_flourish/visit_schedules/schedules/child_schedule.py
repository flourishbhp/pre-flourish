from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule, Visit

from pre_flourish.visit_schedules.crfs.child_crfs import child_crfs_0200
from pre_flourish.visit_schedules.subject_schedule import PfSubjectSchedule

# schedule for new participants
pre_flourish_child_schedule1 = Schedule(
    name='pf_child_schedule1',
    verbose_name='Pre Flourish Schedule 1',
    onschedule_model='pre_flourish.onschedulechildpreflourish',
    offschedule_model='pre_flourish.childoffschedule',
    consent_model='pre_flourish.preflourishchilddummysubjectconsent',
    appointment_model='pre_flourish.appointment')

visit0 = Visit(
    code='0200',
    title='Enrollment Visit',
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(months=3),
    requisitions=None,
    crfs=child_crfs_0200,
    facility_name='5-day clinic')

pre_flourish_child_schedule1.subject_schedule_cls = PfSubjectSchedule
pre_flourish_child_schedule1.add_visit(visit=visit0)
