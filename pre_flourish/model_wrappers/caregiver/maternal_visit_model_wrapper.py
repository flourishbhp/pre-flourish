from django.conf import settings
from edc_subject_dashboard import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper


class MaternalVisitModelWrapper(BaseSubjectVisitModelWrapper):

    model = 'pre_flourish.preflourishvisit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('pre_flourish_subject_dashboard_url')
    next_url_attrs = ['subject_identifier', 'appointment']
