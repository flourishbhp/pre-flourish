from django.contrib import admin
from edc_data_manager.admin import DataActionItemAdmin

from ..models import PFDataActionItem
from ..forms import PFDataActionItemForm
from ..admin_site import pre_flourish_admin


@admin.register(PFDataActionItem, site=pre_flourish_admin)
class PFDataActionItemAdmin(DataActionItemAdmin):

    form = PFDataActionItemForm
