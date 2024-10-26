from core.repositories.contribution_repository import ContributionRepository
from core.shared.customAPIException import CustomAPIException

class ContributionService:

    @staticmethod
    def list_all_contributions():
        try:
            return ContributionRepository.list_contributions()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_contribution(contribution_id):
        try:
            contribution = ContributionRepository.get_contribution_by_id(contribution_id)
            if not contribution:
                raise CustomAPIException(detail='Contribution not found.', status_code=404)
            return contribution
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_contribution(user, validated_data):
        try:
            return ContributionRepository.create_contribution(user, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create contribution: " + str(e), status_code=400)

    @staticmethod
    def update_contribution(contribution_id, validated_data):
        try:
            return ContributionRepository.update_contribution(contribution_id, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to update contribution: " + str(e), status_code=400)

    @staticmethod
    def delete_contribution(contribution_id):
        try:
            contribution = ContributionRepository.get_contribution_by_id(contribution_id)
            if not contribution:
                raise CustomAPIException(detail="Contribution not found.", status_code=404)
            ContributionRepository.delete_contribution(contribution_id) 
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete contribution: " + str(e), status_code=400)

    @staticmethod
    def get_user_total_score(user):
        try:
            score = ContributionRepository.get_user_total_score(user)
            return score
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete contribution: " + str(e), status_code=400)