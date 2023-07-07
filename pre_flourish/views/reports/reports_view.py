from collections import defaultdict

import django_tables2 as tables
from django.apps import apps as django_apps
from django.urls import reverse
from django.utils.html import format_html
from django_tables2 import SingleTableView
from django_tables2.export import ExportMixin
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

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

    @property
    def heu_huu_match_cls(self):
        return django_apps.get_model('pre_flourish.heuhuumatch')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            heu_pool=dict(self.heu_pool),
            huu_pool=dict(self.huu_pool),
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
