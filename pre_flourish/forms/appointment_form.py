import pytz
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_appointment.constants import IN_PROGRESS_APPT, NEW_APPT,\
    INCOMPLETE_APPT, COMPLETE_APPT
from edc_appointment.form_validators import AppointmentFormValidator
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..helper_classes.utils import is_flourish_eligible, caregiver_subject_identifier
from ..models.appointment import Appointment
from ..models import PreFlourishContact


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, AppointmentFormValidator,
                      forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    appointment_model = 'pre_flourish.appointment'

    def clean(self):
        super().clean()

        cleaned_data = self.cleaned_data

        if cleaned_data.get('appt_datetime'):

            visit_definition = self.instance.visits.get(self.instance.visit_code)

            earlist_appt_date = (self.instance.timepoint_datetime -
                                 visit_definition.rlower).astimezone(
                pytz.timezone('Africa/Gaborone'))
            latest_appt_date = (self.instance.timepoint_datetime +
                                visit_definition.rupper).astimezone(
                pytz.timezone('Africa/Gaborone'))

            if self.instance.visit_code_sequence == 0:
                if (cleaned_data.get('appt_datetime') < earlist_appt_date.replace(
                        microsecond=0)
                        or (self.instance.visit_code != '2000'
                            and cleaned_data.get(
                                    'appt_datetime') > latest_appt_date.replace(
                                    microsecond=0))):
                    raise forms.ValidationError(
                        'The appointment datetime cannot be outside the window period, '
                        'please correct. See earliest, ideal and latest datetimes below.')

        self.validate_enrolment_scheduled()

    def validate_enrolment_scheduled(self):
        pf_contact_exists = PreFlourishContact.objects.filter(
            subject_identifier=self.instance.subject_identifier).exists()

        is_eligible, _ = is_flourish_eligible(self.instance.subject_identifier)

        if (is_eligible and not pf_contact_exists and
                self.cleaned_data.get('appt_status') in [COMPLETE_APPT, INCOMPLETE_APPT]):
            raise forms.ValidationError(
                'Please schedule the participant for Flourish enrolment before closing appt.')

    def validate_appt_new_or_complete(self):
        """
        Validates the caregiver appointment model by overriding existing appointment
        validation functions.
        """
        pass

    def validate_sequence(self):
        """Enforce appointment and visit entry sequence.
        """
        if self.cleaned_data.get('appt_status') == IN_PROGRESS_APPT:
            # visit report sequence

            try:
                self.instance.get_previous_by_appt_datetime(
                    subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name
                ).preflourishvisit
            except ObjectDoesNotExist:
                last_visit = self.appointment_model_cls.visit_model_cls().objects.filter(
                    appointment__subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name,
                    report_datetime__lt=self.instance.appt_datetime
                ).order_by('appointment__appt_datetime').last()

                if last_visit:
                    try:
                        last_visit.appointment.get_next_by_appt_datetime(
                            subject_identifier=self.instance.subject_identifier,
                            visit_schedule_name=self.instance.visit_schedule_name)
                    except last_visit.appointment.DoesNotExist:
                        raise forms.ValidationError(
                            f'A previous visit report is required. Enter the visit '
                            f'report for '
                            f'appointment {last_visit.visit_code} before '
                            'starting with this appointment.')
            except AttributeError:
                pass

            # appointment sequence
            try:
                self.instance.get_previous_by_appt_datetime(
                    subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name
                ).preflourishvisit
            except ObjectDoesNotExist:
                first_new_appt = self.appointment_model_cls.objects.filter(
                    subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name,
                    appt_status=NEW_APPT,
                    appt_datetime__lt=self.instance.appt_datetime
                ).order_by('appt_datetime').first()
                if first_new_appt:
                    raise forms.ValidationError(
                        'A previous appointment requires updating. '
                        f'Update appointment for {first_new_appt.visit_code} first.')
            except AttributeError:
                pass

    class Meta:
        model = Appointment
        fields = '__all__'
