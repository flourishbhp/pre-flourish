from edc_visit_schedule import Crf, FormsCollection

child_crfs = {}
child_crfs_1000 = FormsCollection(
    Crf(show_order=1, model='pre_flourish.huupreenrollment'),
    Crf(show_order=2, model='pre_flourish.pfinfanthivtesting', required=False),
    Crf(show_order=3, model='pre_flourish.pfchildpregtesting', required=False),
    Crf(show_order=4, model='pre_flourish.pfchildhivrapidtestcounseling', required=False),
    name='enrollment')
child_crfs.update({1000: child_crfs_1000})
