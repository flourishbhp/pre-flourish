from edc_action_item import Action, site_action_items, HIGH_PRIORITY

MATERNALOFF_STUDY_ACTION = 'submit-caregiver-study'

class MaternalOffStudyAction(Action):
    name = MATERNALOFF_STUDY_ACTION
    display_name = 'Submit Caregiver Offstudy'
    reference_model = 'pre_flourish.maternaloffstudy'
    admin_site_name = 'pre_flourish_admin'
    priority = HIGH_PRIORITY
    singleton = True
