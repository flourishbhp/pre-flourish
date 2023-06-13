from django.db import models
from edc_base.model_validators import date_not_future, datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO

from ..model_mixins import CrfModelMixin
from ...caregiver_choices import POS_NEG_IND


class CyhuuPreEnrollment(CrfModelMixin):

    biological_mother = models.CharField(
        verbose_name='Are you the biological mother of the child?',
        choices=YES_NO,
        max_length=3, )

    hiv_docs = models.CharField(
        verbose_name='Do you have documentation of your HIV status?',
        choices=YES_NO,
        blank=True,
        null=True,
        max_length=3, )

    hiv_test_result = models.CharField(
        verbose_name='HIV test result',
        choices=POS_NEG_IND,
        max_length=14,
        blank=True,
        null=True)

    hiv_test_date = models.DateField(
        verbose_name='Date of test',
        validators=[date_not_future, ],
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'pre_flourish'
        verbose_name = 'CYHUU Pre-Flourish'
        verbose_name_plural = 'CYHUU Pre-Flourish'
