from django.apps import apps as django_apps
from django.db.models import (FileField, ForeignKey, ImageField, ManyToManyField,
                              ManyToOneRel, OneToOneField)
from django.db.models.fields.reverse_related import OneToOneRel
from django.utils.translation import ugettext_lazy as _
from flourish_export.admin_export_helper import AdminExportHelper


class ExportActionMixin(AdminExportHelper):

    def update_variables(self, data={}):
        """ Update study identifiers to desired variable name(s).
        """
        new_data_dict = {}
        replace_idx = {'subject_identifier': 'matpid',
                       'child_subject_identifier': 'childpid',
                       'study_maternal_identifier': 'old_matpid',
                       'study_child_identifier': 'old_childpid'}
        for old_idx, new_idx in replace_idx.items():
            try:
                new_data_dict[new_idx] = data.pop(old_idx)
            except KeyError:
                continue
        new_data_dict.update(data)
        return new_data_dict

    def export_as_csv(self, request, queryset):
        records = []

        for obj in queryset:
            data = obj.__dict__.copy()

            subject_identifier = getattr(obj, 'subject_identifier', None)
            screening_identifier = self.screening_identifier(
                subject_identifier=subject_identifier)

            # Add subject identifier and visit code
            if getattr(obj, 'pre_flourish_visit', None):
                data_copy = data.copy()
                data.clear()

                data.update(
                    subject_identifier=subject_identifier,
                    visit_code=obj.pre_flourish_visit.visit_code,
                    **data_copy)

            # Update variable names for study identifiers
            data = self.update_variables(data)

            data.update(study_status=self.study_status(subject_identifier) or '')

            for field in self.get_model_fields:
                field_name = field.name
                if (field_name == 'consent_version') and self.is_visit(obj):
                    data.update({f'{field_name}':
                                 self.get_consent_version(screening_identifier)})
                    continue
                if isinstance(field, (ForeignKey, OneToOneField, OneToOneRel,)):
                    continue
                if isinstance(field, (FileField, ImageField,)):
                    file_obj = getattr(obj, field_name, '')
                    data.update({f'{field_name}': getattr(file_obj, 'name', '')})
                    continue
                if isinstance(field, ManyToManyField):
                    data.update(self.m2m_data_dict(obj, field))
                    continue
                if not (self.is_consent(obj) or self.is_visit(obj)) and isinstance(field, ManyToOneRel):
                    data.update(self.inline_data_dict(obj, field))
                    continue

            # Exclude identifying values
            data = self.remove_exclude_fields(data)
            # Correct date formats
            data = self.fix_date_formats(data)
            records.append(data)
        response = self.write_to_csv(records)
        return response

    export_as_csv.short_description = _(
        'Export selected %(verbose_name_plural)s')

    actions = [export_as_csv]

    def get_consent_version(self, screening_identifier):
        """
        Returns the consent version of an object
        """
        version_model = django_apps.get_model(
            'pre_flourish.pfconsentversion')
        try:
            version = version_model.objects.get(
                screening_identifier=screening_identifier)
        except version_model.DoesNotExist:
            return ""
        else:
            return version.version

    def screening_identifier(self, subject_identifier=None):
        """Returns a screening identifier.
        """
        consent = self.consent_obj(subject_identifier=subject_identifier)

        if consent:
            return consent.screening_identifier
        return None

    def consent_obj(self, subject_identifier: str):
        consent_cls = django_apps.get_model(
            'pre_flourish.preflourishconsent')
        consent = consent_cls.objects.filter(
            subject_identifier=subject_identifier)

        if consent.exists():
            return consent.last()
        return None

    def is_consent(self, obj):
        consent_cls = django_apps.get_model(
            'pre_flourish.preflourishconsent')
        return isinstance(obj, consent_cls)

    def is_visit(self, obj):
        visit_cls = django_apps.get_model('pre_flourish.preflourishvisit')
        return isinstance(obj, visit_cls)

    def study_status(self, subject_identifier=None):
        if not subject_identifier:
            return ''
        offstudy_model = 'pre_flourish.preflourishoffstudy'
        if len(subject_identifier.split('-')) == 4:
            offstudy_model = 'pre_flourish.preflourishchildoffstudy'
        offstudy_model_cls = django_apps.get_model(offstudy_model)
        is_offstudy = offstudy_model_cls.objects.filter(
            subject_identifier=subject_identifier).exists()

        return 'off_study' if is_offstudy else 'on_study'

    @property
    def exclude_fields(self):
        return ['_state', 'hostname_created', 'hostname_modified',
                'revision', 'device_created', 'device_modified', 'id', 'site_id',
                'modified_time', 'report_datetime_time', 'registration_datetime_time',
                'screening_datetime_time', 'modified', 'form_as_json', 'consent_model',
                'randomization_datetime', 'registration_datetime', 'is_verified_datetime',
                'first_name', 'last_name', 'initials', 'guardian_name', 'identity',
                'pre_flourish_visit_id', 'processed', 'processed_datetime', 'packed',
                'packed_datetime', 'shipped', 'shipped_datetime', 'received_datetime',
                'identifier_prefix', 'primary_aliquot_identifier', 'clinic_verified',
                'clinic_verified_datetime', 'drawn_datetime', 'slug', 'confirm_identity',
                'related_tracking_identifier', 'parent_tracking_identifier', 'site',
                'pre_flourish_consent_id', '_django_version', 'consent_identifier',
                'subject_identifier_as_pk', 'subject_consent_id']
