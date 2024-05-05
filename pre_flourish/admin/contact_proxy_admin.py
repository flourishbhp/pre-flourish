from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_model_admin.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectError
from flourish_follow.admin import ContactAdminMixin

from ..admin_site import pre_flourish_admin
from ..models import PreFlourishContact
from ..forms import PreFlourishContactForm


@admin.register(PreFlourishContact, site=pre_flourish_admin)
class PreFlourishContactAdmin(ContactAdminMixin, admin.ModelAdmin):

    form = PreFlourishContactForm

    def get_next_redirect_url(self, request=None):
        url_name = request.GET.dict().get(
            self.next_querystring_attr).split(',')[0]
        options = self.get_next_options(request=request)

        try:
            redirect_url = reverse(url_name, kwargs=options)
        except NoReverseMatch as e:
            msg = f'{e}. Got url_name={url_name}, kwargs={options}.'
            try:
                redirect_url = reverse(url_name)
            except NoReverseMatch:
                raise ModelAdminNextUrlRedirectError(msg)
        return redirect_url
