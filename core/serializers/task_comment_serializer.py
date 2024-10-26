# comment_serializer.py
from rest_framework import serializers
from core.models.task_comment_model import TaskComment
from core.models.task_model import Task
from core.models.user_model import User

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'author', 'content', 'created_at']
