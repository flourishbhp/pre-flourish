from edc_locator.action_items import SubjectLocatorAction

from edc_action_item import Action, site_action_items, HIGH_PRIORITY

MATERNALOFF_STUDY_ACTION = 'submit-caregiver-study'
CAREGIVER_LOCATOR_ACTION = 'submit-caregiver-locator'


class MaternalOffStudyAction(Action):
    name = MATERNALOFF_STUDY_ACTION
    display_name = 'Submit Caregiver Offstudy'
    reference_model = 'pre_flourish.maternaloffstudy'
    admin_site_name = 'pre_flourish_admin'
    priority = HIGH_PRIORITY
    singleton = True


class CaregiverLocatorAction(SubjectLocatorAction):
    name = CAREGIVER_LOCATOR_ACTION
    display_name = 'Submit Caregiver Locator'
    reference_model = 'pre_flourish.caregiverlocator'
    admin_site_name = 'pre_flourish_admin'


site_action_items.register(CaregiverLocatorAction)
