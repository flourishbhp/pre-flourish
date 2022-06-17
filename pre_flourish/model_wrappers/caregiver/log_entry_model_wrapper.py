from edc_model_wrapper import ModelWrapper
from django.conf import settings
from ...models  import PreFlourishLogEntry

class PreFlourishLogEntryModelWrapper(ModelWrapper):
    model = 'pre_flourish.preflourishlogentry'
    querystring_attrs = ['test',]
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'maternal_dataset_listboard_url')