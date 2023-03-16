import pytz
from django.contrib import admin
from django.utils.safestring import mark_safe

from flourish_child.admin import AppointmentAdmin
from ...admin_site import pre_flourish_admin
from ...forms import CaregiverAppointmentForm
from ...models import CaregiverAppointment


@admin.register(CaregiverAppointment, site=pre_flourish_admin)
class CaregiverAppointmentAdmin(AppointmentAdmin):
    form = CaregiverAppointmentForm
    model = CaregiverAppointment
