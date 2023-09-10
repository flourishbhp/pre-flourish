from django.contrib import admin
from edc_registration.admin import RegisteredSubjectAdmin

from pre_flourish.admin_site import pre_flourish_admin
from pre_flourish.models import PreFlourishRegisteredSubject


@admin.register(PreFlourishRegisteredSubject, site=pre_flourish_admin)
class PreFlourishRegisteredSubjectAdmin(RegisteredSubjectAdmin, admin.ModelAdmin):
    pass
