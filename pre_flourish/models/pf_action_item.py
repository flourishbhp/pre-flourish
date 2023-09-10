from edc_action_item.models.action_item import ActionItem


class PFActionItem(ActionItem):
    subject_identifier_model = 'pre_flourish.preflourishregisteredsubject'

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Pre Flourish Action Item'
        verbose_name_plural = 'Pre Flourish Action Items'
        proxy = True
