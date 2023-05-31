from django.core.exceptions import ObjectDoesNotExist
from edc_action_item import Action, site_action_items, HIGH_PRIORITY
from django.apps import apps as django_apps
from edc_locator.action_items import SubjectLocatorAction

MATERNAL_OFF_STUDY_ACTION = 'submit-pf-caregiver-study'
CHILD_OFF_STUDY_ACTION = 'submit-pf-child-study'
PRE_FLOURISH_CAREGIVER_LOCATOR_ACTION = 'submit-pf-caregiver-locator'
MATERNAL_DEART_STUDY_ACTION = 'submit-pf-death-report'


class MaternalOffStudyAction(Action):
    name = MATERNAL_OFF_STUDY_ACTION
    display_name = 'Submit Pre Flourish Caregiver Offstudy'
    reference_model = 'pre_flourish.preflourishoffstudy'
    admin_site_name = 'pre_flourish_admin'
    priority = HIGH_PRIORITY
    singleton = True

class ChildOffStudyAction(Action):
    name = CHILD_OFF_STUDY_ACTION
    display_name = 'Submit Pre Flourish Child Offstudy'
    reference_model = 'pre_flourish.preflourishchildoffstudy'
    admin_site_name = 'pre_flourish_admin'
    priority = HIGH_PRIORITY
    singleton = True


class PreFlourishCaregiverLocatorAction(SubjectLocatorAction):
    name = PRE_FLOURISH_CAREGIVER_LOCATOR_ACTION
    display_name = 'Submit Pre Flourish Caregiver Locator'
    reference_model = 'pre_flourish.preflourishcaregiverlocator'
    admin_site_name = 'pre_flourish_admin'

class MaternalDearthStudyAction(Action):
    name = MATERNAL_DEART_STUDY_ACTION
    display_name = 'Submit Caregiver Death Report'
    reference_model = 'pre_flourish.preflourishdeathreport'
    admin_site_name = 'pre_flourish_admin'
    show_link_to_add = True
    priority = HIGH_PRIORITY
    singleton = True

    def get_next_actions(self):
        actions = []
        deathreport_cls = django_apps.get_model(
            'pre_flourish.preflourishdeathreport')

        action_item_cls = django_apps.get_model(
            'edc_action_item.actionitem')

        subject_identifier = self.reference_model_obj.subject_identifier
        offstudy = action_item_cls.objects.filter(
            subject_identifier=subject_identifier,
            action_type__name=MATERNAL_DEART_STUDY_ACTION)
        try:
            deathreport_cls.objects.get(
                subject_identifier=subject_identifier)
            if not offstudy:
                actions = [ChildOffStudyAction]
        except ObjectDoesNotExist:
            pass
        return actions


site_action_items.register(PreFlourishCaregiverLocatorAction)
site_action_items.register(ChildOffStudyAction)
site_action_items.register(MaternalOffStudyAction)
site_action_items.register(MaternalDearthStudyAction)
