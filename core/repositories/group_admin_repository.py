from django.core.exceptions import ObjectDoesNotExist
from core.models.group_admin_model import GroupAdmin
from core.shared.customAPIException import CustomAPIException

class GroupAdminRepository:
    @staticmethod
    def add_admin_to_group(group, user):
        if group is None or user is None:
            raise CustomAPIException(detail="Group or user cannot be None.", status_code=400)
        try:
            return GroupAdmin.objects.create(group=group, admin=user)
        except Exception as e:
            raise CustomAPIException(detail=f"Error adding admin to group: {str(e)}", status_code=400)

    @staticmethod
    def remove_admin_from_group(group, user):
        if group is None or user is None:
            raise CustomAPIException(detail="Group or user cannot be None.", status_code=400)
        try:
            admin = GroupAdmin.objects.get(group=group, admin=user)
            admin.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Admin not found in group.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail=f"Error removing admin from group: {str(e)}", status_code=400)

    @staticmethod
    def get_group_admins(group):
        if group is None:
            raise CustomAPIException(detail="Group cannot be None.", status_code=400)
        return GroupAdmin.objects.filter(group=group)
