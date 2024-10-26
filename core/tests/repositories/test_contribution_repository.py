from django.test import TestCase
from core.models.user_model import User
from core.repositories.contribution_repository import ContributionRepository
from core.shared.customAPIException import CustomAPIException
from decimal import Decimal

class ContributionRepositoryTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            name='John Doe',
            cpf='12345678901',
            email='john.doe@example.com',
            dateOfBirth='1990-01-01',
            status='active',
            password='password123'
        )
        self.contribution_data = {
            'type': 'code',
            'description': 'Contributed to the codebase',
            'score': Decimal('50.00')
        }
        self.contribution = ContributionRepository.create_contribution(self.user, self.contribution_data)

    def test_create_contribution(self):
        self.assertIsNotNone(self.contribution.id)
        self.assertEqual(self.contribution.user, self.user)
        self.assertEqual(self.contribution.type, self.contribution_data['type'])
        self.assertEqual(self.contribution.description, self.contribution_data['description'])
        self.assertEqual(self.contribution.score, self.contribution_data['score'])

    def test_get_contribution_by_id(self):
        retrieved_contribution = ContributionRepository.get_contribution_by_id(self.contribution.id)
        self.assertEqual(retrieved_contribution, self.contribution)

    def test_get_contribution_by_id_not_found(self):
        with self.assertRaises(CustomAPIException) as context:
            ContributionRepository.get_contribution_by_id(9999)
        self.assertEqual(context.exception.detail, {'error': 'Contribution not found.'})

    def test_update_contribution(self):
        update_data = {
            'type': 'article',
            'description': 'Updated contribution description',
            'score': Decimal('75.00')
        }
        updated_contribution = ContributionRepository.update_contribution(self.contribution.id, update_data)
        self.assertEqual(updated_contribution.type, update_data['type'])
        self.assertEqual(updated_contribution.description, update_data['description'])
        self.assertEqual(updated_contribution.score, update_data['score'])

    def test_update_contribution_not_found(self):
        with self.assertRaises(CustomAPIException) as context:
            ContributionRepository.update_contribution(9999, {'type': 'project'})
        self.assertEqual(context.exception.detail, {'error': 'Contribution not found.'})

    def test_delete_contribution(self):
        ContributionRepository.delete_contribution(self.contribution.id)
        with self.assertRaises(CustomAPIException) as context:
            ContributionRepository.get_contribution_by_id(self.contribution.id)
        self.assertEqual(context.exception.detail, {'error': 'Contribution not found.'})

    def test_delete_contribution_not_found(self):
        with self.assertRaises(CustomAPIException) as context:
            ContributionRepository.delete_contribution(9999)
        self.assertEqual(context.exception.detail, {'error': 'Contribution not found.'})

    def test_list_contributions(self):
        contributions = ContributionRepository.list_contributions()
        self.assertIn(self.contribution, contributions)
