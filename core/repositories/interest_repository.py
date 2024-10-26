from django.core.exceptions import ObjectDoesNotExist
from core.models.interest_model import Interest
from core.shared.customAPIException import CustomAPIException

class InterestRepository:
    @staticmethod
    def get_all_interests():
        try:
            return Interest.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving interests: " + str(e), status_code=500)

    @staticmethod
    def get_interest_by_id(interest_id):
        try:
            return Interest.objects.get(id=interest_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='Interest not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving interest: " + str(e), status_code=500)

    @staticmethod
    def create_interest(validated_data):
        try:
            interest = Interest.objects.create(**validated_data)
            return interest
        except Exception as e:
            raise CustomAPIException(detail="Error creating interest: " + str(e), status_code=400)

    @staticmethod
    def update_interest(interest_id, validated_data):
        try:
            interest = Interest.objects.get(id=interest_id)
            for attr, value in validated_data.items():
                setattr(interest, attr, value)
            interest.save()
            return interest
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Interest not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating interest: " + str(e), status_code=400)

    @staticmethod
    def delete_interest(interest_id):
        try:
            interest = InterestRepository.get_interest_by_id(interest_id)
            interest.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Interest not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting interest: " + str(e), status_code=400)
