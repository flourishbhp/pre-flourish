from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'pre_flourish' else False

pre_flourish_dashboard = Navbar(name='pre_flourish_dashboard')


pre_flourish_dashboard.append_item(
    NavbarItem(
        name='pre_flourish__screening',
        title='Pre Flourish Screening',
        label='pre flourish screening',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'pre_flourish_screening_listboard_url'],
        no_url_namespace=no_url_namespace))

pre_flourish_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Caregiver Subjects',
        label='Caregiver subjects',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES[
            'pre_flourish_subject_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(pre_flourish_dashboard)
