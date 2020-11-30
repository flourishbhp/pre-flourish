from django.db.models.signals import post_save
from django.dispatch import receiver

from django.apps import apps as django_apps

from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .pre_flourish_consent import PreFlourishConsent


@receiver(post_save, weak=False, sender=PreFlourishConsent,
          dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Update subject on cohort c schedule.
    """
    if not raw:
        put_on_schedule('pre_flourish',
                        instance=instance,
                        subject_identifier=instance.pre_flourish_identifier)


def put_on_schedule(cohort, instance=None, pre_flourish_identifier=None):
    if instance:
        pre_flourish_identifier = pre_flourish_identifier or instance.pre_flourish_identifier

        cohort_label_lower = ''.join(cohort.split('_'))
        onschedule_model = 'pre_flourish.onschedule' + cohort_label_lower

        _, schedule = site_visit_schedules.get_by_onschedule_model(
            onschedule_model)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        schedule_name = cohort + '_schedule_1'

        try:
            onschedule_model_cls.objects.get(
                subject_identifier=instance.pre_flourish_identifier,
                schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            schedule.put_on_schedule(
                subject_identifier=instance.pre_flourish_identifier,
                onschedule_datetime=instance.created,
                schedule_name=schedule_name)
        else:
            schedule.refresh_schedule(
                subject_identifier=instance.pre_flourish_identifier)
