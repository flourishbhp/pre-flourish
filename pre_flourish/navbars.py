from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar

no_url_namespace = True if settings.APP_NAME == 'pre_flourish' else False

pre_flourish_dashboard = Navbar(name='pre_flourish_dashboard')

pre_flourish_dashboard.append_item(
    NavbarItem(
        name='pre_flourish_caregiver_locator',
        title='PF Dataset',
        label='PF dataset',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'pre_flourish_caregiver_locator_listboard_url'],
        no_url_namespace=False))

pre_flourish_dashboard.append_item(
    NavbarItem(
        name='pre_flourish_screening',
        title='PF Screening',
        label='PF screening',
        fa_icon='far fa-user-circle',
        url_name='pre_flourish_screening_listboard_url',
        no_url_namespace=False))

pre_flourish_dashboard.append_item(
    NavbarItem(
        name='pre_flourish_consent',
        title='Caregiver Subjects',
        label='caregiver subjects',
        fa_icon='far fa-user-circle',
        url_name='pre_flourish_consent_listboard_url',
        no_url_namespace=False))

pre_flourish_dashboard.append_item(
    NavbarItem(
        name='pre_flourish_child_subjects',
        title='Child Subjects',
        label='child subjects',
        fa_icon='far fa-user-circle',
        url_name='pre_flourish_child_listboard_url',
        no_url_namespace=False))

pre_flourish_dashboard.append_item(
    NavbarItem(
        name='pre_flourish_reports',
        title='pre_flourish_reports',
        label='PF Reports',
        fa_icon='fa-cogs',
        url_name='pre_flourish:pre_flourish_reports_url'))

pre_flourish_dashboard.append_item(
    NavbarItem(
        name='home_url',
        title='pre_flourish_follow_up',
        label='PF Follow up',
        fa_icon='fa-phone',
        url_name='pre_flourish_follow:home_url'))

site_navbars.register(pre_flourish_dashboard)
