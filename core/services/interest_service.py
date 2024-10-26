from core.repositories.interest_repository import InterestRepository
from core.shared.customAPIException import CustomAPIException

class InterestService:
    @staticmethod
    def list_all_interests():
        try:
            return InterestRepository.get_all_interests()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_interest(interest_id):
        try:
            interest = InterestRepository.get_interest_by_id(interest_id)
            if not interest:
                raise CustomAPIException(detail='Interest not found.', status_code=404)
            return interest
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_interest(validated_data):
        try:
            return InterestRepository.create_interest(validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create interest: " + str(e), status_code=400)

    @staticmethod
    def update_interest(interest_id, validated_data):
        try:
            return InterestRepository.update_interest(interest_id, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to update interest: " + str(e), status_code=400)

    @staticmethod
    def delete_interest(interest_id):
        try:
            interest = InterestRepository.get_interest_by_id(interest_id)
            if not interest:
                raise CustomAPIException(detail="Interest not found.", status_code=404)
            InterestRepository.delete_interest(interest_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete interest: " + str(e), status_code=400)
