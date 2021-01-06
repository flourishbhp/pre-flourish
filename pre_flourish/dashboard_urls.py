from django.conf import settings
from django.conf.urls.static import static
from edc_dashboard import UrlConfig

from .patterns import subject_identifier, screening_identifier
from .views import (ChildListboardView, ScreeningListBoardView,
                    SubjectListboardView, DashboardView)

child_listboard_url_config = UrlConfig(
    url_name='pre_flourish_child_listboard_url',
    view_class=ChildListboardView,
    label='pre_flourish_child_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

pre_flourish_screening_listboard_url_config = UrlConfig(
    url_name='pre_flourish_screening_listboard_url',
    view_class=ScreeningListBoardView,
    label='pre_flourish_screening_listboard',
    identifier_label='screening_identifier',
    identifier_pattern=screening_identifier)

pre_flourish_consent_listboard_url_config = UrlConfig(
    url_name='pre_flourish_consent_listboard_url',
    view_class=SubjectListboardView,
    label='pre_flourish_consent_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

pre_flourish_subject_dashboard_url_config = UrlConfig(
    url_name='pre_flourish_subject_dashboard_url',
    view_class=DashboardView,
    label='pre_flourish_subject_dashboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

urlpatterns = []

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += child_listboard_url_config.listboard_urls
urlpatterns += pre_flourish_screening_listboard_url_config.listboard_urls
urlpatterns += pre_flourish_consent_listboard_url_config.listboard_urls
urlpatterns += pre_flourish_subject_dashboard_url_config.dashboard_urls
