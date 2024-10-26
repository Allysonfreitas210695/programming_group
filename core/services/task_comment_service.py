from core.repositories.task_comment_repository import CommentRepository
from core.shared.customAPIException import CustomAPIException

class CommentService:
    @staticmethod
    def list_comments_by_task(task_id):
        try:
            return CommentRepository.get_comments_by_task(task_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to retrieve comments: " + str(e), status_code=500)

    @staticmethod
    def add_comment_to_task(task_id, comment_data, author):
        try:
            return CommentRepository.add_comment_to_task(task_id, comment_data, author)
        except Exception as e:
            raise CustomAPIException(detail="Failed to add comment: " + str(e), status_code=400)

    @staticmethod
    def delete_comment(comment_id):
        try:
            comment = CommentRepository.get_comment_by_id(comment_id)
            if not comment:
                raise CustomAPIException(detail="Comment not found.", status_code=404)
            CommentRepository.delete_comment(comment_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete comment: " + str(e), status_code=400)
        
    @staticmethod
    def get_comment_by_id(comment_id):
        try:
            return CommentRepository.get_comment_by_id(comment_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to retrieve comment: " + str(e), status_code=404)
