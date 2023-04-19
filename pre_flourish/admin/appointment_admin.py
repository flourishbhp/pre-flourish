import pytz
from django.contrib import admin
from django.utils.safestring import mark_safe

from flourish_child.admin import AppointmentAdmin
from ..admin_site import pre_flourish_admin
from ..forms import AppointmentForm
from ..models.appointment import Appointment


@admin.register(Appointment, site=pre_flourish_admin)
class AppointmentAdmin(AppointmentAdmin):
    form = AppointmentForm
    model = Appointment
