from edc_data_manager.forms import DataActionItemForm

from ..models import PFDataActionItem


class PFDataActionItemForm(DataActionItemForm):
    class Meta:
        model = PFDataActionItem
        fields = '__all__'
