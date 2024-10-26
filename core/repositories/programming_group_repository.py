from django.core.exceptions import ObjectDoesNotExist
from core.models.programming_group_model import ProgrammingGroup
from core.shared.customAPIException import CustomAPIException

class ProgrammingGroupRepository:
    @staticmethod
    def get_all_groups():
        try:
            return ProgrammingGroup.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving groups: " + str(e), status_code=500)

    @staticmethod
    def get_group_by_id(group_id):
        try:
            return ProgrammingGroup.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='Group not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving group: " + str(e), status_code=500)

    @staticmethod
    def create_group(validated_data):
        try:
            if 'creator' not in validated_data:
                raise CustomAPIException(detail="Creator is required.", status_code=400)

            participants = validated_data.pop('participants', [])
            group = ProgrammingGroup.objects.create(**validated_data)

            if participants:
                group.participants.set(participants)

            return group

        except Exception as e:
            raise CustomAPIException(detail="Error creating programming group: " + str(e), status_code=400)

    @staticmethod
    def update_group(group_id, validated_data):
        try:
            group = ProgrammingGroup.objects.get(id=group_id)
            participants = validated_data.pop('participants', [])

            for attr, value in validated_data.items():
                setattr(group, attr, value)

            group.save()

            if participants:
                group.participants.set(participants)

            return group

        except ProgrammingGroup.DoesNotExist:
            raise CustomAPIException(detail="Group not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating group: " + str(e), status_code=400)

    @staticmethod
    def delete_group(group_id):
        try:
            group = ProgrammingGroupRepository.get_group_by_id(group_id)
            group.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Group not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting group: " + str(e), status_code=400)
