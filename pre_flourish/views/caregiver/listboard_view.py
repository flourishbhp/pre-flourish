import re

from django.apps import apps as django_apps
# from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ...helper_classes.utils import get_consent_version_obj, get_is_latest_consent_version
from ...model_wrappers import PreFlourishMaternalScreeningModelWrapper

# from .filters import ListboardViewFilters

pre_flourish_config = django_apps.get_app_config('pre_flourish')


class ScreeningListBoardView(NavbarViewMixin, EdcBaseViewMixin,
                             ListboardFilterViewMixin, SearchFormViewMixin,
                             ListboardView):
    listboard_template = 'pre_flourish_screening_listboard_template'
    listboard_url = 'pre_flourish_screening_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    # listboard_view_filters = ListboardViewFilters()
    model = 'pre_flourish.preflourishsubjectscreening'
    model_wrapper_cls = PreFlourishMaternalScreeningModelWrapper
    navbar_name = 'pre_flourish_dashboard'
    navbar_selected_item = 'pre_flourish_screening'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'pre_flourish_screening_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_latest_consent_version = False

        if self.kwargs.get('screening_identifier'):
            consent_version_obj = get_consent_version_obj(
                self.kwargs.get('screening_identifier'))

            is_latest_consent_version = get_is_latest_consent_version(consent_version_obj)
        context.update(
            is_latest_consent_version=is_latest_consent_version,
            maternal_screening_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('screening_identifier'):
            options.update(
                {'screening_identifier': kwargs.get('screening_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
