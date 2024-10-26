from django.test import TestCase
from core.models.university_model import University
from core.repositories.university_repository import UniversityRepository
from core.shared.customAPIException import CustomAPIException

class UniversityRepositoryTest(TestCase):
    def setUp(self):
        University.objects.all().delete() 
        self.university_data = {
            'name': 'Test University',
            'city': 'Test City',
            'state': 'Test State'
        }
        self.university = University.objects.create(**self.university_data)

    def test_get_all_universities(self):
        universities = UniversityRepository.get_all_universities()
        self.assertEqual(universities.count(), 1)
        self.assertEqual(universities[0].name, 'Test University')

    def test_get_university_by_id(self):
        university = UniversityRepository.get_university_by_id(self.university.id)
        self.assertEqual(university.name, 'Test University')

    def test_create_university(self):
        new_university_data = {
            'name': 'New University',
            'city': 'New City',
            'state': 'New State'
        }
        university = UniversityRepository.create_university(new_university_data)
        self.assertEqual(university.name, 'New University')

    def test_update_university(self):
        updated_data = {
            'name': 'Updated University',
            'city': 'Updated City'
        }
        updated_university = UniversityRepository.update_university(self.university.id, updated_data)
        self.assertEqual(updated_university.name, 'Updated University')
        self.assertEqual(updated_university.city, 'Updated City')

    def test_delete_university(self):
        UniversityRepository.delete_university(self.university.id)
        with self.assertRaises(CustomAPIException) as cm:
            UniversityRepository.get_university_by_id(self.university.id)
        self.assertEqual(cm.exception.detail, {'error': 'University not found.'})

     
