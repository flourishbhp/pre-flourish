from collections import defaultdict

import django_tables2 as tables
from django.apps import apps as django_apps
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django_tables2 import SingleTableView
from django_tables2.export import ExportMixin
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ...helper_classes import HUUPoolGeneration
from ...helper_classes.utils import populate_heu_huu_pool_data
from ...models import MatrixPool


class MatrixPoolTable(tables.Table):
    subject_identifiers = tables.Column()

    def render_subject_identifiers(self, value):
        download_link = reverse('pre_flourish:download_pool_ids_url', args=[value])
        button_html = f'<a href="{download_link}" class="btn btn-primary">Download ' \
                      f'CSV</a>'
        return format_html(button_html)

    class Meta:
        model = MatrixPool
        fields = ('pool', 'bmi_group', 'age_group', 'gender_group',
                  'count')
        attrs = {'class': 'table table-striped'}
        template_name = "django_tables2/bootstrap-responsive.html"


class ReportsView(ExportMixin, EdcBaseViewMixin, NavbarViewMixin,
                  SingleTableView):
    template_name = 'pre_flourish/reports/reports.html'
    navbar_name = 'pre_flourish_dashboard'
    navbar_selected_item = 'pre_flourish_reports'
    model = MatrixPool
    table_class = MatrixPoolTable
    table_pagination = {'per_page': 5}
    export_formats = ('csv', 'xls')  # Specify the export formats you want to support
    pre_flourish_caregiver_child_consent_model = \
        'pre_flourish.preflourishcaregiverchildconsent'
    screening_prior_participants_model = \
        'flourish_caregiver.screeningpriorbhpparticipants'

    @property
    def screening_prior_participants_model_cls(self):
        return django_apps.get_model(self.screening_prior_participants_model)

    @property
    def pre_flourish_caregiver_child_consent_model_cls(self):
        return django_apps.get_model(self.pre_flourish_caregiver_child_consent_model)

    def post(self, request, *args, **kwargs):
        if 'action_button' in request.POST:
            action = request.POST.get('action_button')
            if action == 'refresh':
                populate_heu_huu_pool_data()
        return HttpResponseRedirect(self.request.path)

    @property
    def get_enrolled_to_flourish(self):
        enrolled_screening_ids = self.screening_prior_participants_model_cls.objects \
            .exclude(subject_identifier='').values_list('screening_identifier', flat=True)
        enrolled_pf_participants = self.pre_flourish_caregiver_child_consent_model_cls \
            .objects.filter(
            subject_consent__screening_identifier__in=enrolled_screening_ids
        ).values_list('subject_identifier', flat=True)
        huupool_generation = HUUPoolGeneration(
            subject_identifiers=enrolled_pf_participants)
        return huupool_generation.breakdown_participants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enrolled_to_flourish = {}
        if self.get_enrolled_to_flourish:
            enrolled_to_flourish = self.get_enrolled_to_flourish
        heu_pool_dict = self.convert_to_regular_dict(self.heu_pool)
        heu_pool = self.convert_to_regular_dict(self.heu_pool)
        huu_pool = self.convert_to_regular_dict(self.huu_pool)

        context.update(
            heu_pool=heu_pool,
            huu_pool=huu_pool,
            enrolled_to_flourish=enrolled_to_flourish,
            heu_pool_dict=heu_pool_dict,
        )
        return context

    def get_pool_data(self, pool):
        bmi_age_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        pool_groups = self.model.objects.filter(pool=pool)
        for group in pool_groups:
            bmi_age_data[group.bmi_group][group.age_group][
                group.gender_group] = group.count
        return bmi_age_data

    @property
    def heu_pool(self):
        return self.get_pool_data('heu')

    @property
    def huu_pool(self):
        return self.get_pool_data('huu')

    def convert_to_regular_dict(self, d):
        if isinstance(d, defaultdict):
            d = {k: self.convert_to_regular_dict(v) for k, v in d.items()}
        return d
