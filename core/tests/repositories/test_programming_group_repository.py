from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
import io
from core.models.programming_group_model import ProgrammingGroup
from core.models.user_model import User
from core.repositories.programming_group_repository import ProgrammingGroupRepository
from core.shared.customAPIException import CustomAPIException

class ProgrammingGroupRepositoryTest(TestCase):
    def setUp(self):
        # Criar um usuário para associar ao grupo
        self.user = User.objects.create(
            name='Test User',
            cpf='12345678901',
            email='testuser@example.com',
            dateOfBirth='2000-01-01',
            status='active'
        )
        
        # Criar uma imagem temporária para o teste
        self.image = self.create_test_image()

        self.group_data = {
            'title': 'Test Group',
            'description': 'Test Description',
            'field_of_interest': 'Test Field',
            'technologies_used': 'Python, Django',
            'difficulty_level': 3,
            'image': self.image,
            'privacy': 'public',
            'status': 'active',
            'creator': self.user  
        }

    def create_test_image(self):
        # Criar uma imagem temporária
        image = Image.new('RGB', (100, 100), color = (73, 109, 137))
        byte_io = io.BytesIO()
        image.save(byte_io, format='JPEG')
        byte_io.seek(0)
        return SimpleUploadedFile('test_image.jpg', byte_io.read(), content_type='image/jpeg')

    def test_create_group_with_image(self):
        try:
            group = ProgrammingGroupRepository.create_group(self.group_data)
            self.assertEqual(group.title, 'Test Group')
            self.assertEqual(group.creator, self.user)
            print(group.image.name)
            self.assertTrue(len(group.image.name) > 0)
        except CustomAPIException as e:
            self.fail(f"create_group raised CustomAPIException unexpectedly: {e}")

    def test_get_all_groups(self):
        ProgrammingGroupRepository.create_group(self.group_data)
        groups = ProgrammingGroupRepository.get_all_groups()
        self.assertEqual(groups.count(), 1)

    def test_get_group_by_id(self):
        group = ProgrammingGroupRepository.create_group(self.group_data)
        retrieved_group = ProgrammingGroupRepository.get_group_by_id(group.id)
        self.assertEqual(retrieved_group.id, group.id)

    def test_update_group(self):
        group = ProgrammingGroupRepository.create_group(self.group_data)
        updated_data = {'title': 'Updated Group'}
        updated_group = ProgrammingGroupRepository.update_group(group.id, updated_data)
        self.assertEqual(updated_group.title, 'Updated Group')

    def test_delete_group(self):
        group = ProgrammingGroupRepository.create_group(self.group_data)
        ProgrammingGroupRepository.delete_group(group.id)
        with self.assertRaises(CustomAPIException):
            ProgrammingGroupRepository.get_group_by_id(group.id)
