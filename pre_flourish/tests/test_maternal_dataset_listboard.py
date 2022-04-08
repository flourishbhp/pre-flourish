from django.test import TestCase, tag
from django.conf import settings
from django.shortcuts import reverse

@tag('dataset')
class TestMaternalDataset(TestCase):
    def test_listboard_accessable(self):
        url = reverse(settings.DASHBOARD_URL_NAMES.get('pre_flourish_maternal_dataset_listboard_url'))
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200, msg='Maternal Dataset not accessable')

