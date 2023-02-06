from django.contrib import admin
from edc_model_admin import StackedInlineMixin, ModelAdminFormAutoNumberMixin

from .child_consent_mixin import ChildConsentMixin
from .model_admin_mixins import ModelAdminMixin
from ...admin_site import pre_flourish_admin
from ...models import PreFlourishCaregiverChildConsent


class PreFlourishCaregiverChildConsentInline(StackedInlineMixin,
                                             ModelAdminFormAutoNumberMixin,
                                             ChildConsentMixin,
                                             admin.StackedInline):
    pass


@admin.register(PreFlourishCaregiverChildConsent, site=pre_flourish_admin)
class PreFlourishCaregiverChildConsentAdmin(ModelAdminMixin, ChildConsentMixin,
                                            admin.ModelAdmin):
    pass
