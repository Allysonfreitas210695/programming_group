from rest_framework import serializers
from core.models.notification_model import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'sender', 'notification_type', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']
