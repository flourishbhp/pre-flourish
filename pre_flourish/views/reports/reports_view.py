import django_tables2 as tables
from django.apps import apps as django_apps
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django_tables2 import SingleTableView
from django_tables2.export import ExportMixin
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from .heu_mixin import HEUMixin
from .huu_mixin import HUUMixin


class DataTable(tables.Table):
    bmi_group = tables.Column(verbose_name="BMI Group")
    age_group = tables.Column(verbose_name="Age Group")
    gender = tables.Column()
    patient_ids = tables.Column()

    def render_patient_ids(self, value):
        download_link = reverse('pre_flourish:download_pool_ids_url', args=[value])
        button_html = f'<a href="{download_link}" class="btn btn-primary">Download ' \
                      f'CSV</a>'
        return format_html(button_html)

    class Meta:
        attrs = {'class': 'table table-striped'}
        template_name = "django_tables2/bootstrap-responsive.html"


def create_table_data(data):
    table_data = []
    if data:
        for bmi_range, age_group_data in data.items():
            for age_group, gender_data in age_group_data.items():
                for gender, patient_ids in gender_data.items():
                    patient_ids_str = ', '.join(patient_ids)
                    table_data.append(
                        {'bmi_group': bmi_range, 'age_group': age_group, 'gender': gender,
                         'patient_ids': patient_ids_str})

    return table_data


class ReportsView(ExportMixin, HEUMixin, HUUMixin, EdcBaseViewMixin, NavbarViewMixin,
                  SingleTableView):
    template_name = 'pre_flourish/reports/reports.html'
    navbar_name = 'pre_flourish_dashboard'
    navbar_selected_item = 'pre_flourish_reports'
    table_class = DataTable

    @property
    def heu_huu_match_cls(self):
        return django_apps.get_model('pre_flourish.heuhuumatch')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_participants_with_height_weight_dob()
        self.get_huu_report()
        get_huu_report = self.get_huu_report().get('bmi_age_data')
        huu_ids = self.get_huu_report().get('subject_data')
        get_bmi_age_data = self.get_participants_with_height_weight_dob().get(
            'bmi_age_data')
        heu_ids = self.get_participants_with_height_weight_dob().get('subject_data')
        table = self.table_class(create_table_data(heu_ids))
        table2 = self.table_class(create_table_data(huu_ids))
        if get_huu_report:
            context.update(
                huu_report=dict(get_huu_report),
            )
        if get_bmi_age_data:
            context.update(
                bmi_age_data=dict(get_bmi_age_data),
            )
        if heu_ids:
            context.update(
                heu_ids=dict(heu_ids),
            )
        if huu_ids:
            context.update(
                huu_ids=dict(huu_ids),
            )

        context.update(
            table=table,
            table2=table2,
            gender_data=self.get_gender_matched
        )
        return context

    @property
    def get_matched(self):
        return self.heu_huu_match_cls.objects.all()

    @property
    def get_gender_matched(self):
        return list(self.get_matched.values('gender').annotate(
            count=Count('gender')).order_by(
            'gender'))

    def get_queryset(self):
        # Return an empty queryset since we are not using a model or queryset
        return []
