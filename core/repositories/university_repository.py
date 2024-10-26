from core.models.university_model import University
from core.shared.customAPIException import CustomAPIException
from django.core.exceptions import ObjectDoesNotExist

class UniversityRepository:
    @staticmethod
    def get_all_universities():
        try:
            return University.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving universities: " + str(e), status_code=500)

    @staticmethod
    def get_university_by_id(university_id):
        try:
            return University.objects.get(id=university_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='University not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving university: " + str(e), status_code=500)

    @staticmethod
    def create_university(validated_data):
        try:
            university, created = University.objects.get_or_create(**validated_data)
            if not created:
                raise CustomAPIException(detail="University already exists.", status_code=400)
            return university
        except Exception as e:
            raise CustomAPIException(detail="Error creating university: " + str(e), status_code=400)

    @staticmethod
    def update_university(university_id, validated_data):
        try:
            university = University.objects.get(id=university_id)
            for attr, value in validated_data.items():
                setattr(university, attr, value)
            university.save()
            return university
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="University not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating university: " + str(e), status_code=400)

    @staticmethod
    def delete_university(university_id):
        try:
            university = UniversityRepository.get_university_by_id(university_id)
            university.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="University not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting university: " + str(e), status_code=400)
