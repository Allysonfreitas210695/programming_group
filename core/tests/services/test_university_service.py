from django.test import TestCase
from unittest.mock import patch, MagicMock
from core.models.university_model import University
from core.services.university_services import UniversityService
from core.repositories.university_repository import UniversityRepository
from core.shared.customAPIException import CustomAPIException

class UniversityServiceTest(TestCase):
    def setUp(self):
        University.objects.all().delete() 
        self.university_data = {
            'name': 'Test University',
            'city': 'Test City',
            'state': 'Test State'
        }
        self.university = University.objects.create(**self.university_data)


    @patch.object(UniversityRepository, 'get_all_universities', return_value=[])
    def test_list_all_universities(self, mock_get_all_universities):
        result = UniversityService.list_all_universities()
        self.assertEqual(result, [])
        mock_get_all_universities.assert_called_once()

    @patch.object(UniversityRepository, 'get_university_by_id')
    def test_retrieve_university(self, mock_get_university_by_id):
        mock_get_university_by_id.return_value = MagicMock(name='University')
        result = UniversityService.retrieve_university(self.university.id)
        self.assertIsNotNone(result)
        mock_get_university_by_id.assert_called_once_with(self.university.id)

    @patch.object(UniversityRepository, 'create_university')
    def test_create_university(self, mock_create_university):
        mock_create_university.return_value = MagicMock(name='University')
        result = UniversityService.create_university(self.university_data)
        self.assertIsNotNone(result)
        mock_create_university.assert_called_once_with(self.university_data)

    @patch.object(UniversityRepository, 'update_university')
    def test_update_university(self, mock_update_university):
        mock_update_university.return_value = MagicMock(name='University')
        result = UniversityService.update_university(self.university.id, self.university_data)
        self.assertIsNotNone(result)
        mock_update_university.assert_called_once_with(self.university.id, self.university_data)