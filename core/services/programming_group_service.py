from core.repositories.programming_group_repository import ProgrammingGroupRepository
from core.shared.customAPIException import CustomAPIException

class ProgrammingGroupService:
    @staticmethod
    def list_all_groups():
        try:
            return ProgrammingGroupRepository.get_all_groups()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_group(group_id):
        try:
            group = ProgrammingGroupRepository.get_group_by_id(group_id)
            if not group:
                raise CustomAPIException(detail='Programming group not found.', status_code=404)
            return group
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_group(validated_data):
        try:
            # Chama o repositório para criar o grupo
            return ProgrammingGroupRepository.create_group(validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create programming group: " + str(e), status_code=400)

    @staticmethod
    def update_group(group_id, validated_data):
        try:
            # Chama o repositório para atualizar o grupo
            return ProgrammingGroupRepository.update_group(group_id, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to update programming group: " + str(e), status_code=400)

    @staticmethod
    def delete_group(group_id):
        try:
            group = ProgrammingGroupRepository.get_group_by_id(group_id)
            if not group:
                raise CustomAPIException(detail="Programming group not found.", status_code=404)
            ProgrammingGroupRepository.delete_group(group_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete programming group: " + str(e), status_code=400)
