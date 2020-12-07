from edc_visit_schedule import FormsCollection, Crf

crf = {}
crfs_1000 = FormsCollection(
    Crf(show_order=2, model='pre_flourish.cyhuupreenrollment'),
    name='enrollment')
crf.update({1000: crfs_1000})
