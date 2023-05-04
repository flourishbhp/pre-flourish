from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ...model_wrappers import PreflourishCaregiverLocatorModelWrapper
from ...model_wrappers import PreFlourishMaternalScreeningModelWrapper


# from ...model_wrappers import MaternalDatasetModelWrapper


class PreFlourishCaregiverLocatorListBoardView(NavbarViewMixin, EdcBaseViewMixin,
                                               ListboardFilterViewMixin,
                                               SearchFormViewMixin,
                                               ListboardView):
    listboard_template = 'pre_flourish_caragiver_locator_listboard_template'
    listboard_url = 'pre_flourish_caregiver_locator_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"
    model = 'flourish_caregiver.caregiverlocator'
    # listboard_view_filters = ListboardViewFilters()
    navbar_name = 'pre_flourish_dashboard'
    # navbar_selected_item = 'pre_flourish_caregiver_locator'
    # ordering = '-locatorlog__locatorlogentry__report_datetime'
    paginate_by = 10
    search_form_url = 'pre_flourish_caregiver_locator_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @property
    def model_wrapper_cls(self):
        model_wrapper_cls = PreflourishCaregiverLocatorModelWrapper
        model_wrapper_cls.subject_screening_wrapper = \
            PreFlourishMaternalScreeningModelWrapper
        return model_wrapper_cls

    def get_queryset(self):
        """
        This study is for prev. BCCP participants only, hence they are being
        collected from the caregiver locator whose subject identifier starts with
        066-

        Returns:
            Queryset with BCCP participants
        """
        # participants = super().get_queryset().filter(
        #     subject_identifier__istartswith='066'
        # )

        participants = super().get_queryset().filter(
            study_maternal_identifier__istartswith='066'
        )

        return participants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            maternal_locator_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('screening_identifier'):
            options.update(
                {'screening_identifier': kwargs.get('screening_identifier')})
        if kwargs.get('study_maternal_identifier'):
            options.update(
                {'study_maternal_identifier': kwargs.get('study_maternal_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if search_term:
            q = Q(study_maternal_identifier__iexact=search_term)
        return q
