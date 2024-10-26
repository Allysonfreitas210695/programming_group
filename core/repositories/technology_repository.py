from django.core.exceptions import ObjectDoesNotExist
from core.models.technology_model import Technology
from core.shared.customAPIException import CustomAPIException

class TechnologyRepository:
    @staticmethod
    def get_all_technologies():
        try:
            return Technology.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving technologies: " + str(e), status_code=500)

    @staticmethod
    def get_technology_by_id(technology_id):
        try:
            return Technology.objects.get(id=technology_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='Technology not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving technology: " + str(e), status_code=500)

    @staticmethod
    def create_technology(validated_data):
        try:
            technology = Technology.objects.create(**validated_data)
            return technology
        except Exception as e:
            raise CustomAPIException(detail="Error creating technology: " + str(e), status_code=400)

    @staticmethod
    def update_technology(technology_id, validated_data):
        try:
            technology = Technology.objects.get(id=technology_id)
            for attr, value in validated_data.items():
                setattr(technology, attr, value)
            technology.save()
            return technology
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Technology not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating technology: " + str(e), status_code=400)

    @staticmethod
    def delete_technology(technology_id):
        try:
            technology = TechnologyRepository.get_technology_by_id(technology_id)
            technology.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Technology not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting technology: " + str(e), status_code=400)
