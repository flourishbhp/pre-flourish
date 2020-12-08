"""pre_flourish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from django.views.generic.base import RedirectView

from edc_action_item.admin_site import edc_action_item_admin
from edc_appointment.admin_site import edc_appointment_admin
from edc_identifier.admin_site import edc_identifier_admin
from .admin_site import pre_flourish_admin

from .views import HomeView, AdministrationView


app_name = 'pre_flourish'
app_config = django_apps.get_app_config(app_name)


urlpatterns = [
    path('accounts/', include('edc_base.auth.urls')),
    path('admin/', include('edc_base.auth.urls')),

    path('admin/', admin.site.urls),
    path('admin/', pre_flourish_admin.urls),

    path('admin/', edc_identifier_admin.urls),
    path('admin/', edc_appointment_admin.urls),
    path('admin/', edc_action_item_admin.urls),

    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('admin/pre_flourish/',
         RedirectView.as_view(url='admin/pre_flourish/'),
         name='pre_flourish_models_url'),

    path('subject/', include('pre_flourish.dashboard_urls')),
    path('edc_action_item/', include('edc_action_item.urls')),
    path('appointment/', include('edc_appointment.urls')),
    path('edc_base/', include('edc_base.urls')),
    path('edc_consent/', include('edc_consent.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_identifier/', include('edc_identifier.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),
    path('edc_subject_dashboard/', include('edc_subject_dashboard.urls')),
    path('edc_visit_schedule/', include('edc_visit_schedule.urls')),

    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
]
