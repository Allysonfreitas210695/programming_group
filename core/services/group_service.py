from core.repositories.group_repository import GroupRepository
from core.models.group_model import Group
from core.shared.customAPIException import CustomAPIException

class GroupService:
    @staticmethod
    def list_groups(user):
        return Group.objects.filter(creator=user)

    @staticmethod
    def create_group(name, creator, members):
        return GroupRepository.create_group(name, creator, members)

    @staticmethod
    def get_group(group_id):
        group = GroupRepository.get_group_by_id(group_id)
        if not group:
            raise CustomAPIException('Group not found', status_code=404)
        return group

    @staticmethod
    def update_group(group_id, **kwargs):
        group = GroupRepository.get_group_by_id(group_id)
        if not group:
            raise CustomAPIException("Group not found", status_code=404)
        return GroupRepository.update_group(group, **kwargs)

    @staticmethod
    def delete_group(group_id):
        group = GroupRepository.get_group_by_id(group_id)
        if not group:
            raise CustomAPIException("Group not found", status_code=404)
        GroupRepository.delete_group(group)
