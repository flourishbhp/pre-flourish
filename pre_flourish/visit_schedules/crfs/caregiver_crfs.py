from edc_visit_schedule import FormsCollection, Crf

caregiver_crfs = {}
caregiver_crfs_1000 = FormsCollection(
    Crf(show_order=1, model='pre_flourish.cyhuupreenrollment'),
    name='enrollment')
caregiver_crfs.update({1000: caregiver_crfs_1000})
