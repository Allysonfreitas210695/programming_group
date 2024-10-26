from rest_framework import serializers

from core.models.group_chat_message_model import GroupChatMessage

class GroupChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChatMessage
        fields = ['id', 'group', 'sender', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']