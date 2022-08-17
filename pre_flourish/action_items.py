from edc_action_item import Action, site_action_items, HIGH_PRIORITY

from edc_locator.action_items import SubjectLocatorAction

MATERNALOFF_STUDY_ACTION = 'submit-caregiver-study'
PRE_FLOURISH_CAREGIVER_LOCATOR_ACTION = 'pre-flourish-submit-caregiver-locator'


class MaternalOffStudyAction(Action):
    name = MATERNALOFF_STUDY_ACTION
    display_name = 'Submit Caregiver Offstudy'
    reference_model = 'pre_flourish.maternaloffstudy'
    admin_site_name = 'pre_flourish_admin'
    priority = HIGH_PRIORITY
    singleton = True


class PreFlourishCaregiverLocatorAction(SubjectLocatorAction):
    name = PRE_FLOURISH_CAREGIVER_LOCATOR_ACTION
    display_name = 'Submit Pre Flourish Caregiver Locator'
    reference_model = 'pre_flourish.preflourishcaregiverlocator'
    admin_site_name = 'pre_flourish_admin'


site_action_items.register(PreFlourishCaregiverLocatorAction)
