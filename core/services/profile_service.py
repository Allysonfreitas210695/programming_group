from core.repositories.profile_repository import UserProfileRepository
from core.shared.customAPIException import CustomAPIException

class UserProfileService:
    @staticmethod
    def list_all_profiles():
        try:
            return UserProfileRepository.get_all_profiles()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_profile(user_id):
        try:
            profile = UserProfileRepository.get_profile_by_user_id(user_id)
            if not profile:
                raise CustomAPIException(detail='Profile not found.', status_code=404)
            return profile
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)
        
    @staticmethod
    def retrieve_profile(profile_id):
        try:
            profile = UserProfileRepository.get_profile_by_id(profile_id)
            if not profile:
                raise CustomAPIException(detail='Profile not found.', status_code=404)
            return profile
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)


    @staticmethod
    def create_profile(validated_data):
        try:
            return UserProfileRepository.create_profile(validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create profile: " + str(e), status_code=400)

    @staticmethod
    def update_profile(profile_id, validated_data):
        try:
            profile = UserProfileRepository.get_profile_by_id(profile_id)
            for attr, value in validated_data.items():
                if attr not in ['technologies', 'interests']:
                    setattr(profile, attr, value)

            # Atualizar tecnologias e interesses (Many-to-Many fields)
            if 'technologies' in validated_data:
                profile.technologies.set(validated_data['technologies'])  # Define novas tecnologias
            if 'interests' in validated_data:
                profile.interests.set(validated_data['interests'])  # Define novos interesses

            profile.save()
            return profile
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Profile not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating profile: " + str(e), status_code=400)


    @staticmethod
    def delete_profile(user_id):
        try:
            profile = UserProfileRepository.get_profile_by_user_id(user_id)
            if not profile:
                raise CustomAPIException(detail="Profile not found.", status_code=404)
            UserProfileRepository.delete_profile(user_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete profile: " + str(e), status_code=400)
