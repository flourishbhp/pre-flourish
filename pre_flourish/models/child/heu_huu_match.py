import json

from django.db import models
from django.utils import timezone
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
        default=timezone.now,
        help_text='Date and time of this report')

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'HeuHuu Matching Participants'
        verbose_name_plural = 'HeuHuu Matching Participants'


class MatrixPool(BaseUuidModel):
    pool = models.CharField(
        verbose_name="Pool",
        blank=True,
        null=True,
        max_length=50)

    bmi_group = models.CharField(
        verbose_name="BMI Group",
        blank=True,
        null=True,
        max_length=50)

    age_group = models.CharField(
        verbose_name="Age Group",
        blank=True,
        null=True,
        max_length=50)

    gender_group = models.CharField(
        verbose_name="Gender Group",
        blank=True,
        null=True,
        max_length=50)

    count = models.IntegerField(
        verbose_name="Count",
        blank=True,
        null=True)

    subject_identifiers = models.TextField(
        verbose_name="Subject Identifiers",
        blank=True,
        null=True)

    def set_subject_identifiers(self, subject_identifiers):
        self.subject_identifiers = json.dumps(subject_identifiers)

    @property
    def get_subject_identifiers(self):
        return json.loads(self.subject_identifiers)

    class Meta:
        app_label = 'pre_flourish'
        verbose_name = 'Metrix Pool'
        verbose_name_plural = 'Metrix Pool'
        unique_together = ('pool', 'bmi_group', 'age_group', 'gender_group')
