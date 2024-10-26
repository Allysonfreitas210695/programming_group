from core.repositories.technology_repository import TechnologyRepository
from core.shared.customAPIException import CustomAPIException

class TechnologyService:
    @staticmethod
    def list_all_technologies():
        try:
            return TechnologyRepository.get_all_technologies()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_technology(technology_id):
        try:
            technology = TechnologyRepository.get_technology_by_id(technology_id)
            if not technology:
                raise CustomAPIException(detail='Technology not found.', status_code=404)
            return technology
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_technology(validated_data):
        try:
            return TechnologyRepository.create_technology(validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create technology: " + str(e), status_code=400)

    @staticmethod
    def update_technology(technology_id, validated_data):
        try:
            return TechnologyRepository.update_technology(technology_id, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to update technology: " + str(e), status_code=400)

    @staticmethod
    def delete_technology(technology_id):
        try:
            technology = TechnologyRepository.get_technology_by_id(technology_id)
            if not technology:
                raise CustomAPIException(detail="Technology not found.", status_code=404)
            TechnologyRepository.delete_technology(technology_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete technology: " + str(e), status_code=400)
