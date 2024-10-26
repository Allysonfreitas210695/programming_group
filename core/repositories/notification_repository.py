from django.core.exceptions import ObjectDoesNotExist
from core.models.notification_model import Notification
from core.shared.customAPIException import CustomAPIException

class NotificationRepository:
    @staticmethod
    def get_all_notifications_for_user(user):
        try:
            return Notification.objects.filter(user=user).order_by('-created_at')
        except Exception as e:
            raise CustomAPIException(detail=f"Error retrieving notifications: {str(e)}", status_code=500)

    @staticmethod
    def get_notification_by_id(notification_id):
        try:
            return Notification.objects.get(id=notification_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Notification not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail=f"Error retrieving notification: {str(e)}", status_code=500)

    @staticmethod
    def create_notification(validated_data):
        try:
            return Notification.objects.create(**validated_data)
        except Exception as e:
            raise CustomAPIException(detail=f"Error creating notification: {str(e)}", status_code=400)

    @staticmethod
    def update_notification(notification_id, validated_data):
        try:
            notification = Notification.objects.get(id=notification_id)
            for attr, value in validated_data.items():
                setattr(notification, attr, value)
            notification.save()
            return notification
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Notification not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail=f"Error updating notification: {str(e)}", status_code=400)

    @staticmethod
    def delete_notification(notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Notification not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail=f"Error deleting notification: {str(e)}", status_code=400)
