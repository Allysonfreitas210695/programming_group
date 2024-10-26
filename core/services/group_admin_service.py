from core.repositories.group_admin_repository import GroupAdminRepository
from core.shared.customAPIException import CustomAPIException

class GroupAdminService:
    @staticmethod
    def add_admin(group, user):
        if group is None or user is None:
            raise CustomAPIException(detail="Group or user cannot be None.", status_code=400)
        try:
            return GroupAdminRepository.add_admin_to_group(group, user)
        except Exception as e:
            raise CustomAPIException(detail=f"Error adding admin: {str(e)}", status_code=400)

    @staticmethod
    def remove_admin(group, user):
        if group is None or user is None:
            raise CustomAPIException(detail="Group or user cannot be None.", status_code=400)
        try:
            GroupAdminRepository.remove_admin_from_group(group, user)
        except Exception as e:
            raise CustomAPIException(detail=f"Error removing admin: {str(e)}", status_code=400)

    @staticmethod
    def list_admins(group):
        if group is None:
            raise CustomAPIException(detail="Group cannot be None.", status_code=400)
        try:
            return GroupAdminRepository.get_group_admins(group)
        except Exception as e:
            raise CustomAPIException(detail=f"Error listing admins: {str(e)}", status_code=500)
