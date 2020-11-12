from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = 'pre_flourish/home.html'
    navbar_name = 'pre_flourish_dashboard'
    navbar_selected_item = 'home'
