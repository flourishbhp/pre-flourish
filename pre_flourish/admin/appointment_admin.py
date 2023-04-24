import pytz
from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_appointment.admin import AppointmentAdmin as BaseAppointmentAdmin
from ..admin_site import pre_flourish_admin
from ..forms import AppointmentForm
from ..models.appointment import Appointment


@admin.register(Appointment, site=pre_flourish_admin)
class AppointmentAdmin(BaseAppointmentAdmin):
    form = AppointmentForm
    model = Appointment
