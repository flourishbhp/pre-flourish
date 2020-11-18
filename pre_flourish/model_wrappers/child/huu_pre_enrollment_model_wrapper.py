from dateutil import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_utcnow
from edc_model_wrapper import ModelWrapper


class HuuPreEnrollmentModelWrapper(ModelWrapper):

    model = 'pre_flourish.huupreenrollment'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'child_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']
