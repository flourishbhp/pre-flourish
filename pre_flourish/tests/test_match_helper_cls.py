from django.contrib.auth.models import Group, User
from django.core import mail
from django.test import TestCase, tag

from pre_flourish.helper_classes import MatchHelper


@tag('match_helper')
class MatchHelperTestCase(TestCase):

    def setUp(self):
        self.helper = MatchHelper()

        self.test_user = User.objects.create_user(
            username='test_user', email='test_user@example.com')
        self.pre_flourish_group = Group.objects.create(name='pre_flourish')
        self.pre_flourish_group.user_set.add(self.test_user)

    def test_create_matrix_pool(self):
        subject_identifiers = ['subject1', 'subject2']
        self.helper.create_matrix_pool(
            name='Test Pool',
            age_group=(9.5, 13),
            bmi_group='<14.9',
            gender_group='Male',
            subject_identifiers=subject_identifiers
        )

        matrix_pool = self.helper.matrix_pool_cls.objects.get(pool='Test Pool')
        self.assertIsNotNone(matrix_pool)

        self.assertEqual(matrix_pool.get_subject_identifiers, subject_identifiers)

    def test_prepare_create_pool(self):
        bmi_age_data = {
            '<14.9': {(9.5, 13): {'Male': 2}},
        }
        subject_data = {
            '<14.9': {(9.5, 13): {'Male': ['subject1', 'subject2']}},
        }
        self.helper.prepare_create_pool('Test Pool', bmi_age_data, subject_data)

        matrix_pool = self.helper.matrix_pool_cls.objects.get(pool='Test Pool')
        self.assertIsNotNone(matrix_pool)
        expected_subject_identifiers = ['subject1', 'subject2']
        self.assertEqual(matrix_pool.get_subject_identifiers, expected_subject_identifiers)


    @tag('smtnp')
    def test_subject_moves_to_new_pool(self):
        initial_pool_name = 'heu'
        initial_subject_identifier = '1234'
        self.helper.create_matrix_pool(
            name=initial_pool_name,
            age_group=(9.5, 13),
            bmi_group='<14.9',
            gender_group='Male',
            subject_identifiers=[initial_subject_identifier]
        )

        new_pool_name = 'heu'
        new_subject_identifier = '1234'
        self.helper.create_matrix_pool(
            name=new_pool_name,
            age_group=(14, 16),
            bmi_group='<14.9',
            gender_group='Male',
            subject_identifiers=[new_subject_identifier]
        )

        initial_pool = self.helper.matrix_pool_cls.objects.get(
            pool=initial_pool_name, age_group='(9.5, 13)',)
        new_pool = self.helper.matrix_pool_cls.objects.get(
            pool=new_pool_name, age_group='(14, 16)',)

        self.assertEqual(initial_pool.get_subject_identifiers, [])
        self.assertEqual(initial_pool.count, 0)

        self.assertEqual(new_pool.get_subject_identifiers, ['1234'])
        self.assertEqual(new_pool.count, 1)

    def test_send_email_to_pre_flourish_users(self):
        class MockMatrix:
            def __init__(self, subject_identifiers):
                self.subject_identifiers = subject_identifiers

        matrix_objects = [MockMatrix(['subject1', 'subject2'])]

        with self.assertLogs('pre_flourish.helper_classes.match_helper',
                             level='INFO') as log:
            self.helper.send_email_to_pre_flourish_users(matrix_objects)

        self.assertIn('Reminder email sent to pre_flourish users.', log.output[0])

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Reminder: Enroll into Flourish')
