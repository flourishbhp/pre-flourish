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
        verbose_name="HUE Subject Identifier",
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
