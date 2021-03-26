from edc_visit_schedule import FormsCollection, Crf

child_crfs = {}
child_crfs_1000 = FormsCollection(
    Crf(show_order=1, model='pre_flourish.huupreenrollment'),
    name='enrollment')
child_crfs.update({1000: child_crfs_1000})
