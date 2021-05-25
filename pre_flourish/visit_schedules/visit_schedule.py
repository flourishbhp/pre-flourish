from edc_visit_schedule import VisitSchedule, site_visit_schedules

from .schedules import pre_flourish_schedule1, pre_flourish_schedule2, pre_flourish_schedule3
from .schedules import pre_flourish_child_schedule1

pre_flourish_visit_schedule = VisitSchedule(
    name='visit_schedule1',
    verbose_name='Pre Flourish Visit Schedule',
    offstudy_model='pre_flourish.preflourishoffstudy',
    locator_model='',
    death_report_model='pre_flourish.preflourishdeathreport',
    previous_visit_schedule=None)

pre_flourish_visit_schedule.add_schedule(pre_flourish_schedule1)
pre_flourish_visit_schedule.add_schedule(pre_flourish_schedule2)
pre_flourish_visit_schedule.add_schedule(pre_flourish_schedule3)

site_visit_schedules.register(pre_flourish_visit_schedule)

pre_flourish_child_visit_schedule = VisitSchedule(
    name='child_visit_schedule1',
    verbose_name='Pre Flourish Child Visit Schedule',
    offstudy_model='pre_flourish.preflourishoffstudy',
    locator_model='',
    death_report_model='pre_flourish.preflourishdeathreport',
    previous_visit_schedule=None)

pre_flourish_child_visit_schedule.add_schedule(pre_flourish_child_schedule1)

site_visit_schedules.register(pre_flourish_child_visit_schedule)
