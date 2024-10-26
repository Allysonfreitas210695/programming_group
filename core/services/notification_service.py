from core.repositories.notification_repository import NotificationRepository
from core.shared.customAPIException import CustomAPIException

class NotificationService:
    @staticmethod
    def list_all_notifications(user):
        try:
            return NotificationRepository.get_all_notifications_for_user(user)
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def retrieve_notification(notification_id):
        try:
            return NotificationRepository.get_notification_by_id(notification_id)
        except CustomAPIException as e:
            raise e
        except Exception as e:
            raise CustomAPIException(detail=str(e), status_code=500)

    @staticmethod
    def create_notification(validated_data):
        try:
            return NotificationRepository.create_notification(validated_data)
        except CustomAPIException as e:
            raise e
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to create notification: {str(e)}", status_code=400)

    @staticmethod
    def update_notification(notification_id, validated_data):
        try:
            return NotificationRepository.update_notification(notification_id, validated_data)
        except CustomAPIException as e:
            raise e
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to update notification: {str(e)}", status_code=400)

    @staticmethod
    def delete_notification(notification_id):
        try:
            NotificationRepository.delete_notification(notification_id)
        except CustomAPIException as e:
            raise e
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to delete notification: {str(e)}", status_code=400)
