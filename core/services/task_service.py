# task_service.py
from core.models.task_model import Task
from core.repositories.task_repository import TaskRepository
from core.shared.customAPIException import CustomAPIException

class TaskService:
    @staticmethod
    def list_all_tasks():
        try:
            return TaskRepository.get_all_tasks()
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def list_tasks_by_group(group_id):
        try:
            return TaskRepository.get_tasks_by_group(group_id)
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_task(task_id):
        try:
            task = TaskRepository.get_task_by_id(task_id)
            if not task:
                raise CustomAPIException(detail='Task not found.', status_code=404)
            return task
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_task(validated_data):
        try:
            responsible_users = validated_data.pop('responsible', None)

            task = Task.objects.create(**validated_data)

            if responsible_users:
                task.responsible.set(responsible_users) 

            return task
        except Exception as e:
            raise CustomAPIException(detail="Error creating task: " + str(e), status_code=400)


    @staticmethod
    def update_task(task_id, validated_data):
        try:
            return TaskRepository.update_task(task_id, validated_data)
        except Exception as e:
            raise CustomAPIException(detail="Failed to update task: " + str(e), status_code=400)

    @staticmethod
    def delete_task(task_id):
        try:
            task = TaskRepository.get_task_by_id(task_id)
            if not task:
                raise CustomAPIException(detail="Task not found.", status_code=404)
            TaskRepository.delete_task(task_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete task: " + str(e), status_code=400)
