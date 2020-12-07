from edc_visit_schedule import VisitSchedule, site_visit_schedules

# from ..models import S

from .schedule import pre_flourish_schedule

pre_flourish_visit_schedule = VisitSchedule(
    name='visit_schedule1',
    verbose_name='Pre Flourish Visit Schedule',
    offstudy_model='pre_flourish.offstudy',
    locator_model='pre_flourish.pre_flourish_caregiver_locator',
    death_report_model='pre_flourish.deathreport',
    previous_visit_schedule=None)

pre_flourish_visit_schedule.add_schedule(pre_flourish_schedule)

site_visit_schedules.register(pre_flourish_visit_schedule)
