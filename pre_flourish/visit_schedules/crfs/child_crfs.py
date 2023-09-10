from edc_visit_schedule import Crf, FormsCollection

child_crfs_0200 = FormsCollection(
    Crf(show_order=1, model='pre_flourish.huupreenrollment'),
    Crf(show_order=2, model='pre_flourish.pfchildpregtesting', required=False),
    Crf(show_order=3, model='pre_flourish.pfchildhivrapidtestcounseling', required=False),
    name='enrollment')
