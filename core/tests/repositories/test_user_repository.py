from django.test import TestCase
from core.models.user_model import User
from core.repositories.user_repository import UserRepository
from core.shared.customAPIException import CustomAPIException

class UserRepositoryTest(TestCase):

    def setUp(self):
        self.user_data = {
            'name': 'John Doe',
            'cpf': '12345678901',
            'email': 'john.doe@example.com',
            'dateOfBirth': '1990-01-01',
            'status': 'active',
            'password': 'password123'
        }
        self.user = UserRepository.create_user(self.user_data)

    def test_get_all_users(self):
        users = UserRepository.get_all_users()
        user_emails = [user.email for user in users]
        self.assertIn(self.user.email, user_emails)

    def test_get_user_by_id(self):
        user = UserRepository.get_user_by_id(self.user.id)
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
        user = UserRepository.create_user(user_data)
        self.assertEqual(user.email, user_data['email'])

    def test_update_user(self):
        updated_data = {'name': 'John Updated', 'password': 'newpassword123'}
        user = UserRepository.update_user(self.user.id, updated_data)
        self.assertEqual(user.name, updated_data['name'])
        self.assertTrue(user.check_password(updated_data['password']))

    def test_delete_user(self):
        UserRepository.delete_user(self.user.id)
        user = UserRepository.get_user_by_id(self.user.id)
        self.assertEqual(user.status, 'inactive')
