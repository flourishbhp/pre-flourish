import pytz
from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_appointment.admin import AppointmentAdmin as BaseAppointmentAdmin

from .admin_redirect_mixin import AdminRedirectMixin
from .exportaction_mixin import ExportActionMixin
from ..admin_site import pre_flourish_admin
from ..forms import AppointmentForm
from ..models.appointment import Appointment


@admin.register(Appointment, site=pre_flourish_admin)
class AppointmentAdmin(ExportActionMixin, AdminRedirectMixin, BaseAppointmentAdmin):
    form = AppointmentForm
    model = Appointment

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        app_obj = Appointment.objects.get(id=object_id)

        if app_obj.visit_code_sequence == 0:
            earliest_start = (app_obj.timepoint_datetime -
                              app_obj.visits.get(app_obj.visit_code).rlower).astimezone(
                pytz.timezone('Africa/Gaborone'))

            latest_start = (app_obj.timepoint_datetime +
                            app_obj.visits.get(app_obj.visit_code).rupper).astimezone(
                pytz.timezone('Africa/Gaborone'))

            ideal_start = app_obj.timepoint_datetime.astimezone(
                pytz.timezone('Africa/Gaborone'))

            extra_context.update({
                'earliest_start': earliest_start.strftime("%Y-%m-%d, %H:%M:%S"),
                'latest_start': latest_start.strftime("%Y-%m-%d, %H:%M:%S"),
                'ideal_start': ideal_start.strftime("%Y-%m-%d, %H:%M:%S"), })

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def update_change_instructions(self, extra_context):
        extra_context = extra_context or {}
        extra_context[
            'instructions'] = self.change_instructions or self.instructions

        if extra_context.get('earliest_start'):
            earliest_start = extra_context.get('earliest_start')
            latest_start = extra_context.get('latest_start')
            ideal_start = extra_context.get('ideal_start')

            additional_instructions = mark_safe(
                '<table style="background-color: #f8f8f8;padding:10px;margin-top:10px;'
                'width:60%;border:0.5px solid #f0f0f0"><tr>'
                f'<td colspan="3">Earliest Start: <b>{earliest_start}</b></td>'
                f'<td colspan="3">Ideal Start: <b>{ideal_start}</b></td>'
                f'<td colspan="3">Latest Start: <b>{latest_start}</b></td>'
                '</table></tr> <BR>'
                'To start or continue to edit FORMS for this subject, change the '
                'appointment status below to "In Progress" and click SAVE. <BR>'
                '<i>Note: You may only edit one appointment at a time. '
                'Before you move to another appointment, change the appointment '
                'status below to "Incomplete" or "Done".</i>')

            extra_context['additional_instructions'] = additional_instructions
        return extra_context

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'subject_identifier': 'childpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}
        if len(data.get('subject_identifier', '').split('-')) == 3:
            replace_idx.update({'subject_identifier': 'matpid',
                                'child_subject_identifier': 'childpid', })
        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict
