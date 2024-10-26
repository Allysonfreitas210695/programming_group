from django.test import TestCase
from core.models.group_model import Group
from core.models.user_model import User
from core.models.group_admin_model import GroupAdmin
from core.repositories.group_admin_repository import GroupAdminRepository
from core.shared.customAPIException import CustomAPIException
import uuid

class GroupAdminRepositoryTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='Test Group', creator=self.create_user())
        self.admin = User.objects.create_user(
            email=f'admin_{uuid.uuid4()}@test.com',
            password='password',
            name='Admin',
            cpf='12345678901',
            dateOfBirth='2000-01-01'
        )
        self.non_admin = User.objects.create_user(
            email=f'user_{uuid.uuid4()}@test.com',
            password='password',
            name='User',
            cpf='09876543210',
            dateOfBirth='1990-01-01'
        )
        self.group_admin = GroupAdmin.objects.create(group=self.group, admin=self.admin)

    def create_user(self):
        return User.objects.create_user(
            email=f'creator_{uuid.uuid4()}@test.com',
            password='password',
            name='Creator',
            cpf='11111111111',
            dateOfBirth='1980-01-01'
        )

    def test_get_group_admins(self):
        admins = GroupAdminRepository.get_group_admins(self.group)
        self.assertIn(self.group_admin, admins)

    def test_add_admin(self):
        GroupAdminRepository.add_admin_to_group(self.group, self.non_admin)
        self.assertTrue(GroupAdmin.objects.filter(group=self.group, admin=self.non_admin).exists())

    def test_remove_admin(self):
        GroupAdminRepository.remove_admin_from_group(self.group, self.admin)
        self.assertFalse(GroupAdmin.objects.filter(group=self.group, admin=self.admin).exists())

    def test_get_group_admins_not_found(self):
      group = Group.objects.create(name='Another Group', creator=self.create_user())
      admins = GroupAdminRepository.get_group_admins(group)
      self.assertQuerySetEqual(admins, GroupAdmin.objects.none())


    def test_add_admin_error(self):
        with self.assertRaises(CustomAPIException):
            GroupAdminRepository.add_admin_to_group(self.group, None)

    def test_remove_admin_error(self):
        with self.assertRaises(CustomAPIException):
            GroupAdminRepository.remove_admin_from_group(self.group, None)
