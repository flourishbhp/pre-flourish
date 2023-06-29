from django.db import models
from edc_base import get_utcnow
from edc_base.model_mixins import BaseUuidModel


class HeuHuuMatch(BaseUuidModel):
    huu_prt = models.CharField(
        verbose_name="HUU Subject Identifier",
        blank=True,
        null=True,
        max_length=50)

    heu_prt = models.CharField(
        verbose_name="HEU Subject Identifier",
        blank=True,
        null=True,
        max_length=50)

    heu_prt_age = models.IntegerField(
        verbose_name="HUE Subject Age",
        blank=True,
        null=True, )

    huu_prt_age = models.IntegerField(
        verbose_name="HUU Subject Age",
        blank=True,
        null=True, )

    huu_prt_bmi = models.DecimalField(
        verbose_name="HUU Subject BMI",
        blank=True,
        max_digits=10, decimal_places=4,
        null=True, )

    heu_prt_bmi = models.DecimalField(
        verbose_name="HEU Subject BMI",
        blank=True,
        max_digits=10, decimal_places=4,
        null=True, )

    gender = models.CharField(
        verbose_name="Subject(s) gender",
        blank=True,
        null=True,
        max_length=50)

    match_datetime = models.DateField(
        verbose_name='Date Match',
        default=get_utcnow().date(),
        help_text='Date and time of this report')

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'HeuHuu Matching Participants'
        verbose_name_plural = 'HeuHuu Matching Participants'
