# task_repository.py
from django.core.exceptions import ObjectDoesNotExist
from core.models.task_model import Task
from core.models.programming_group_model import ProgrammingGroup
from core.shared.customAPIException import CustomAPIException

class TaskRepository:
    @staticmethod
    def get_all_tasks():
        try:
            return Task.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving tasks: " + str(e), status_code=500)

    @staticmethod
    def get_task_by_id(task_id):
        try:
            return Task.objects.get(id=task_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='Task not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving task: " + str(e), status_code=500)

    @staticmethod
    def get_tasks_by_group(group_id):
        try:
            group = ProgrammingGroup.objects.get(id=group_id)
            return group.tasks.all()  
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='Group not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving tasks for group: " + str(e), status_code=500)

    @staticmethod
    def create_task(validated_data):
        try:
            if 'created_by' not in validated_data:
                raise CustomAPIException(detail="Creator is required.", status_code=400)
            if 'group' not in validated_data:
                raise CustomAPIException(detail="Group is required.", status_code=400)
            
            task = Task.objects.create(**validated_data)
            return task
        except Exception as e:
            raise CustomAPIException(detail="Error creating task: " + str(e), status_code=400)


    @staticmethod
    def update_task(task_id, validated_data):
        try:
            task = Task.objects.get(id=task_id)
            for attr, value in validated_data.items():
                setattr(task, attr, value)
            task.save()
            return task
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Task not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating task: " + str(e), status_code=400)

    @staticmethod
    def delete_task(task_id):
        try:
            task = TaskRepository.get_task_by_id(task_id)
            task.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Task not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting task: " + str(e), status_code=400)
