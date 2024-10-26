from core.models.private_chat_message_model import PrivateChatMessage
from rest_framework import serializers

class PrivateChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
