from core.models.contribution_model import Contribution
from core.shared.customAPIException import CustomAPIException
from django.db import models

class ContributionRepository:

    @staticmethod
    def create_contribution(user, data):
        try:
            contribution = Contribution.objects.create(
                user=user,
                type=data['type'],
                description=data['description'],
                score=data['score']
            )
            return contribution
        except Exception as e:
            raise CustomAPIException(detail=f"Error creating contribution: {str(e)}", status_code=400)

    @staticmethod
    def get_contribution_by_id(contribution_id):
        try:
            return Contribution.objects.get(id=contribution_id)
        except Contribution.DoesNotExist:
            raise CustomAPIException(detail='Contribution not found.', status_code=404)

    @staticmethod
    def update_contribution(contribution_id, data):
        try:
            contribution = ContributionRepository.get_contribution_by_id(contribution_id)
            contribution.type = data['type']
            contribution.description = data['description']
            contribution.score = data['score']
            contribution.save()
            return contribution
        except CustomAPIException:
            raise
        except Exception as e:
            raise CustomAPIException(detail=f"Error updating contribution: {str(e)}", status_code=400)

    @staticmethod
    def delete_contribution(contribution_id):
        try:
            contribution = ContributionRepository.get_contribution_by_id(contribution_id)
            contribution.delete()
        except CustomAPIException:
            raise
        except Exception as e:
            raise CustomAPIException(detail=f"Error deleting contribution: {str(e)}", status_code=400)

    @staticmethod
    def list_contributions():
        try:
            return Contribution.objects.all()
        except Exception as e:
            raise CustomAPIException(detail=f"Error retrieving contributions: {str(e)}", status_code=400)

    @staticmethod
    def get_user_total_score(user):
        try:
           return Contribution.objects.filter(user=user).aggregate(total_score=models.Sum('score'))['total_score'] or 0
        except Exception as e:
            raise CustomAPIException(detail=f"Error retrieving contributions: {str(e)}", status_code=400)
        
