from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Pre Flourish'
    site_header = 'Pre Flourish'
    index_title = 'Pre Flourish'
    site_url = '/administration/'
    enable_nav_sidebar = False


pre_flourish_admin = AdminSite(name='pre_flourish_admin')
