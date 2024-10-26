from django.test import TestCase
from core.models.user_model import User
from core.services.contribution_service import ContributionService
from core.models.contribution_model import Contribution
from core.shared.customAPIException import CustomAPIException
from decimal import Decimal

class ContributionServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            name='Jane Doe',
            cpf='09876543210',
            email='jane.doe@example.com',
            dateOfBirth='1992-02-02',
            status='active',
            password='password456'
        )
        self.contribution_data = {
            'type': 'code',
            'description': 'Contribution to codebase',
            'score': Decimal('25.00')
        }

    def test_create_contribution(self):
        contribution = ContributionService.create_contribution(self.user, self.contribution_data)
        self.assertIsNotNone(contribution.id)
        self.assertEqual(contribution.user, self.user)
        self.assertEqual(contribution.type, self.contribution_data['type'])
        self.assertEqual(contribution.description, self.contribution_data['description'])
        self.assertEqual(contribution.score, self.contribution_data['score'])

    def test_delete_contribution(self):
        contribution = ContributionService.create_contribution(self.user, self.contribution_data)
        ContributionService.delete_contribution(contribution.id)
        with self.assertRaises(CustomAPIException) as context:
            ContributionService.retrieve_contribution(contribution.id)
        
        self.assertEqual(context.exception.detail['error'], "{'error': 'Contribution not found.'}")

    def test_retrieve_contribution(self):
        contribution = ContributionService.create_contribution(self.user, self.contribution_data)
        retrieved_contribution = ContributionService.retrieve_contribution(contribution.id)
        self.assertEqual(retrieved_contribution.id, contribution.id)

    def test_list_contributions(self):
        ContributionService.create_contribution(self.user, self.contribution_data)
        contributions = ContributionService.list_all_contributions()
        self.assertGreater(len(contributions), 0)

    def test_retrieve_contribution_not_found(self):
        with self.assertRaises(CustomAPIException) as context:
            ContributionService.retrieve_contribution(9999)
        self.assertEqual(context.exception.detail['error'], "{'error': 'Contribution not found.'}")
