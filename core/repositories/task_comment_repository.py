# comment_repository.py
from django.core.exceptions import ObjectDoesNotExist
from core.models.task_comment_model import TaskComment
from core.models.task_model import Task
from core.shared.customAPIException import CustomAPIException

class CommentRepository:
    @staticmethod
    def get_all_comments():
        try:
            return TaskComment.objects.all()
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving comments: " + str(e), status_code=500)

    @staticmethod
    def get_comment_by_id(comment_id):
        try:
            return TaskComment.objects.get(id=comment_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail='Comment not found.', status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving comment: " + str(e), status_code=500)

    @staticmethod
    def add_comment_to_task(task_id, comment_data, author):
        try:
            task = Task.objects.get(id=task_id)

            comment_data.pop('task', None)

            comment = TaskComment.objects.create(task=task, author=author, **comment_data)
            return comment
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Task not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error adding comment: " + str(e), status_code=400)



    @staticmethod
    def delete_comment(comment_id):
        try:
            comment = CommentRepository.get_comment_by_id(comment_id)
            comment.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Comment not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting comment: " + str(e), status_code=400)
