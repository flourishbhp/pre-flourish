from django.conf import settings
from edc_subject_dashboard import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper


class MaternalVisitModelWrapper(BaseSubjectVisitModelWrapper):

    model = 'pre_flourish.caregivervisit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('pre_flourish_subject_dashboard_url')
    next_url_attrs = ['pre_flourish_identifier', 'appointment']
