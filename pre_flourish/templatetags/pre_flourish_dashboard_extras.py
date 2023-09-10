from datetime import datetime
from urllib.parse import unquote, urlencode

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from edc_base.utils import age, get_utcnow
from edc_visit_schedule.models import SubjectScheduleHistory

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is not None:
        return dictionary.get(key)


@register.inclusion_tag('pre_flourish/buttons/consent_button.html')
def consent_button(model_wrapper):
    title = ['Consent subject to participate.']
    return dict(
        subject_identifier=model_wrapper.consent.object.subject_identifier,
        subject_screening_obj=model_wrapper.object,
        add_consent_href=model_wrapper.consent.href,
        # consent_version=model_wrapper.consent_version,
        title=' '.join(title))


@register.inclusion_tag('pre_flourish/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    pre_flourish_subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')
    return dict(
        pre_flourish_subject_dashboard_url=pre_flourish_subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)


@register.inclusion_tag('pre_flourish/buttons/locator_button.html')
def locator_button(model_wrapper):
    return dict(
        add_locator_href=model_wrapper.caregiver_locator.href,
        screening_identifier=model_wrapper.object.screening_identifier,
        caregiver_locator_obj=model_wrapper.locator_model_obj)


@register.inclusion_tag('pre_flourish/buttons/edit_screening_button.html')
def edit_screening_button(model_wrapper):
    title = ['Edit Subject Screening form.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('pre_flourish/buttons/screening_button.html')
def screening_button(model_wrapper):
    add_screening_href = ''
    subject_screening_obj = None
    if hasattr(model_wrapper, 'maternal_screening'):
        add_screening_href = model_wrapper.maternal_screening.href
    if model_wrapper.screening_model_obj:
        subject_screening_obj = model_wrapper.screening_model_obj

    return dict(
        add_screening_href=add_screening_href,
        subject_screening_obj=subject_screening_obj
    )


@register.inclusion_tag('pre_flourish/buttons/eligibility_button.html')
def eligibility_button(model_wrapper):
    comment = []
    obj = model_wrapper.object
    tooltip = None
    if obj.ineligibility:
        comment = obj.ineligibility[1:-1].split(',')
        comment = list(set(comment))
        comment.sort()
    return dict(eligible=obj.is_eligible, comment=comment,
                tooltip=tooltip, obj=obj)


@register.inclusion_tag('pre_flourish/buttons/log_entry_button.html')
def log_entry_button(model_wrapper):
    href = model_wrapper.log_entry_model_wrapper.href
    return dict(
        href=href,
    )


@register.inclusion_tag('pre_flourish/buttons/edit_screening_button.html')
def edit_screening_button(model_wrapper):
    title = ['Edit Subject Screening form.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('pre_flourish/buttons/assents_button.html')
def assents_button(model_wrapper):
    title = ['Child Assent(s)']
    return dict(
        wrapped_assents=model_wrapper.wrapped_child_assents,
        child_assents_exist=model_wrapper.child_assents_exists,
        title=' '.join(title), )


@register.inclusion_tag('pre_flourish/buttons/assent_button.html')
def assent_button(model_wrapper):
    title = ['Assent child to participate.']
    return dict(
        consent_obj=model_wrapper.object,
        assent_age=model_wrapper.child_age >= 7,
        child_assent=model_wrapper.child_assent,
        title=' '.join(title))


@register.inclusion_tag(
    'flourish_dashboard/buttons/child_dashboard_button.html')
def child_dashboard_button(model_wrapper):
    child_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_child_dashboard_url')
    return dict(
        child_dashboard_url=child_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)


@register.inclusion_tag(
    'pre_flourish/buttons/caregiver_dashboard_button.html')
def caregiver_dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'pre_flourish_subject_dashboard_url')

    subject_identifier = model_wrapper.object.subject_identifier

    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=subject_identifier)


@register.inclusion_tag(
    'flourish_dashboard/buttons/caregiver_contact_button.html')
def caregiver_contact_button(model_wrapper):
    title = ['Caregiver Contact.']
    return dict(
        subject_identifier=model_wrapper.object.subject_identifier,
        add_caregiver_contact_href=model_wrapper.caregiver_contact.href,
        title=' '.join(title), )


@register.inclusion_tag('flourish_dashboard/buttons/caregiver_off_study.html')
def caregiver_off_study_button(model_wrapper):
    title = 'Caregiver Off Study'
    return dict(
        title=title,
        href=model_wrapper.caregiver_offstudy.href,
        subject_identifier=model_wrapper.subject_identifier
    )


@register.inclusion_tag(
    'flourish_dashboard/buttons/caregiver_death_report_button.html')
def caregiver_death_report_button(model_wrapper):
    title = 'Caregiver Death Report'
    return dict(
        title=title,
        href=model_wrapper.caregiver_death_report.href,
        subject_identifier=model_wrapper.subject_identifier
    )


@register.simple_tag(takes_context=True)
def get_age(context, born=None):
    if born:
        born = datetime.strptime(born, '%Y-%m-%d')
        reference_datetime = context.get('reference_datetime', get_utcnow())
        participant_age = age(born, reference_datetime)
        age_str = ''
        age_months = participant_age.months % 12
        if participant_age.years > 0:
            age_str += str(participant_age.years) + ' yrs '
        if age_months > 0:
            age_str += str(age_months) + ' months'
        return age_str


@register.inclusion_tag('edc_visit_schedule/subject_schedule_footer_row.html')
def subject_schedule_footer_row(subject_identifier, visit_schedule, schedule,
                                subject_dashboard_url):
    context = {}
    try:
        history_obj = SubjectScheduleHistory.objects.get(
            visit_schedule_name=visit_schedule.name,
            schedule_name=schedule.name,
            subject_identifier=subject_identifier,
            offschedule_datetime__isnull=False)
    except SubjectScheduleHistory.DoesNotExist:
        onschedule_model_obj = schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier,
            schedule_name=schedule.name, )
        options = dict(subject_identifier=subject_identifier)
        query = unquote(urlencode(options))
        href = (
            f'{visit_schedule.offstudy_model_cls().get_absolute_url()}?next='
            f'{subject_dashboard_url},subject_identifier')
        href = '&'.join([href, query])
        context = dict(
            offschedule_datetime=None,
            onschedule_datetime=onschedule_model_obj.onschedule_datetime,
            href=mark_safe(href))
    else:
        onschedule_model_obj = schedule.onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier,
            schedule_name=schedule.name)
        options = dict(subject_identifier=subject_identifier)
        query = unquote(urlencode(options))
        offstudy_model_obj = None
        try:
            offstudy_model_obj = visit_schedule.offstudy_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except visit_schedule.offstudy_model_cls.DoesNotExist:
            href = (f'{visit_schedule.offstudy_model_cls().get_absolute_url()}'
                    f'?next={subject_dashboard_url},subject_identifier')
        else:
            href = (f'{offstudy_model_obj.get_absolute_url()}?next='
                    f'{subject_dashboard_url},subject_identifier')

        href = '&'.join([href, query])

        context = dict(
            offschedule_datetime=history_obj.offschedule_datetime,
            onschedule_datetime=onschedule_model_obj.onschedule_datetime,
            href=mark_safe(href))
        if offstudy_model_obj:
            context.update(offstudy_date=offstudy_model_obj.offstudy_date)
    context.update(
        visit_schedule=visit_schedule,
        schedule=schedule,
        verbose_name=visit_schedule.offstudy_model_cls._meta.verbose_name)
    return context


@register.inclusion_tag('flourish_dashboard/buttons/child_death_report_button.html')
def child_death_report_button(model_wrapper):
    title = 'Child Death Report'
    return dict(
        title=title,
        href=model_wrapper.child_death_report.href,
        subject_identifier=model_wrapper.subject_identifier
    )


age_groups = ['9.5, 13', '14, 16', '17, 21']


@register.inclusion_tag('pre_flourish/reports/matrix_pool.html')
def heu_matrix_pool(data):
    title = 'FLOURISH MATRIX POOL'
    return dict(
        title=title,
        data=data,
        age_groups=age_groups
    )


@register.inclusion_tag('pre_flourish/reports/matrix_pool.html')
def huu_matrix_pool(data):
    title = 'PRE FLOURISH MATRIX POOL'
    return dict(
        title=title,
        data=data,
        age_groups=age_groups
    )


@register.inclusion_tag('pre_flourish/reports/matrix_pool.html')
def enrolled_to_flourish(data):
    title = 'Participants Enrolled to FLOURISH'
    return dict(
        title=title,
        data=data,
        none_match=True,
        age_groups=['0, 9.5', '9.6, 13', '14, 16', '17, 21']
    )


@register.inclusion_tag(
    'flourish_dashboard/buttons/bhp_prior_screening_button.html')
def bhp_prior_screening_button(model_wrapper):
    return dict(
        add_screening_href=model_wrapper.bhp_prior_screening.href,
        screening_identifier=model_wrapper.screening_identifier,
        prior_screening_obj=model_wrapper.bhp_prior_screening_model_obj,
        caregiver_locator_obj=model_wrapper.locator_model_obj)
