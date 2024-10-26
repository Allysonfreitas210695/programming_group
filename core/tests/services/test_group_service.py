from django.test import TestCase
from core.models.group_model import Group
from core.models.user_model import User
from core.services.group_service import GroupService
from core.shared.customAPIException import CustomAPIException

class GroupServiceTestCase(TestCase):
    def setUp(self):
        self.creator = User.objects.create(
            email='creator@test.com',
            password='password123',
            name='Creator',
            cpf='11111111111',
            dateOfBirth='1980-01-01'
        )
        self.group = Group.objects.create(
            name='Test Group',
            creator=self.creator
        )

    def test_list_groups(self):
        groups = GroupService.list_groups(self.creator)
        self.assertIn(self.group, groups)

    def test_create_group(self):
        user = User.objects.create(
            name='Test User',
            email='user@example.com',
            password='password123',
            cpf='22222222222',
            dateOfBirth='1980-01-01'
        )
        group = GroupService.create_group(
            name='New Group',
            creator=self.creator,
            members=[user]  # Ajustar para incluir membros na criação
        )
        # Confirmar que o grupo foi criado corretamente
        self.assertEqual(group.name, 'New Group')
        self.assertEqual(group.creator, self.creator)
        self.assertIn(user, group.members.all())

    def test_get_group(self):
        group = GroupService.get_group(self.group.id)
        self.assertEqual(group, self.group)

    def test_get_group_not_found(self):
        with self.assertRaises(CustomAPIException):
            GroupService.get_group(9999)

    def test_update_group(self):
        updated_group = GroupService.update_group(
            self.group.id,
            name='Updated Group Name'
        )
        self.assertEqual(updated_group.name, 'Updated Group Name')

    def test_delete_group(self):
        GroupService.delete_group(self.group.id)
        with self.assertRaises(CustomAPIException):
            GroupService.get_group(self.group.id)
