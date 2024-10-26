from core.models.group_model import Group

class GroupRepository:
    @staticmethod
    def create_group(name, creator, members):
        group = Group.objects.create(name=name, creator=creator)
        group.members.set(members) 
        return group

    @staticmethod
    def get_group_by_id(group_id):
        try:
            return Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return None

    @staticmethod
    def update_group(group, **kwargs):
        for attr, value in kwargs.items():
            setattr(group, attr, value)
        group.save()
        return group

    @staticmethod
    def delete_group(group):
        group.delete()
