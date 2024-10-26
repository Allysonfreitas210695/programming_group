from django.test import TestCase
from core.services.user_services import UserService
from core.shared.customAPIException import CustomAPIException

class UserServiceTest(TestCase):

    def setUp(self):
        self.user_data = {
            'name': 'John Doe',
            'cpf': '12345678901',
            'email': 'john.doe@example.com',
            'dateOfBirth': '1990-01-01',
            'status': 'active',
            'password': 'password123'
        }
        self.user = UserService.create_user(self.user_data)

    def test_list_all_users(self):
        users = UserService.list_all_users()
        user_emails = [user.email for user in users]
        self.assertIn(self.user.email, user_emails)

    def test_retrieve_user(self):
        user = UserService.retrieve_user(self.user.id)
        self.assertEqual(user.email, self.user.email)

    def test_create_user(self):
        user_data = {
            'name': 'Jane Smith',
            'cpf': '09876543210',
            'email': 'jane.smith@example.com',
            'dateOfBirth': '1992-02-02',
            'status': 'inactive',
            'password': 'password456'
        }
        user = UserService.create_user(user_data)
        self.assertEqual(user.email, user_data['email'])

    def test_update_user(self):
        updated_data = {'name': 'John Updated', 'password': 'newpassword123'}
        user = UserService.update_user(self.user.id, updated_data)
        self.assertEqual(user.name, updated_data['name'])
        self.assertTrue(user.check_password(updated_data['password']))

    def test_delete_user(self):
        UserService.delete_user(self.user.id)
        user = UserService.retrieve_user(self.user.id)
        self.assertEqual(user.status, 'inactive')
