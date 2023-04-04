from django import forms
from edc_base.sites.forms import SiteModelFormMixin

from pre_flourish.models.caregiver.offschedule import CaregiverOffSchedule


class CaregiverOffScheduleForm(SiteModelFormMixin, forms.ModelForm):
    class Meta:
        model = CaregiverOffSchedule
        fields = '__all__'
