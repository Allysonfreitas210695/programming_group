from core.repositories.university_repository import UniversityRepository
from core.shared.customAPIException import CustomAPIException

class UniversityService:
    @staticmethod
    def list_all_universities():
        try:
            return UniversityRepository.get_all_universities()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_university(university_id):
        try:
            university = UniversityRepository.get_university_by_id(university_id)
            if not university:
                raise CustomAPIException(detail='University not found.', status_code=404)
            return university
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_university(validated_data):
        try:
            return UniversityRepository.create_university(validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create university: " + str(e), status_code=400)

    @staticmethod
    def update_university(university_id, validated_data):
        try:
            return UniversityRepository.update_university(university_id, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to update university: " + str(e), status_code=400)

    @staticmethod
    def delete_university(university_id):
        try:
            university = UniversityRepository.get_university_by_id(university_id)
            if not university:
                raise CustomAPIException(detail='University not found.', status_code=404)
            UniversityRepository.delete_university(university_id)
        except CustomAPIException as e:
            raise e
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete university: " + str(e), status_code=400)
