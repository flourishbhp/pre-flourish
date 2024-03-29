from edc_visit_schedule import FormsCollection, Crf

caregiver_crfs_0200 = FormsCollection(
    Crf(show_order=1, model='pre_flourish.cyhuupreenrollment'),
    Crf(show_order=2, model='pre_flourish.pfhivrapidtestcounseling', required=False),
    Crf(show_order=3, model='pre_flourish.preflourishcliniciannotes'),
    name='enrollment')
