from django.apps import apps as django_apps
from flourish_follow.model_wrappers import CaregiverContactModelWrapperMixin

from .contact_proxy_model_wrapper import PreFlourishContactModelWrapper


class PreFlourishContactModelWrapperMixin(CaregiverContactModelWrapperMixin):

    contact_model_wrapper_cls = PreFlourishContactModelWrapper

    @property
    def caregiver_contact_cls(self):
        return django_apps.get_model('pre_flourish.preflourishcontact')
