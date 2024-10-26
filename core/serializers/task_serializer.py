from rest_framework import serializers
from core.models.task_model import Task
from core.models.user_model import User
from core.models.programming_group_model import ProgrammingGroup

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')  
    responsible = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())  
    group = serializers.PrimaryKeyRelatedField(queryset=ProgrammingGroup.objects.all())  
    is_completed = serializers.BooleanField(required=False) 

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'attachments', 'deadline', 'group', 'responsible', 'created_by', 'is_completed']
        extra_kwargs = {
            'created_by': {'read_only': True},  
            'attachments': {'required': False},  
            'is_completed': {'default': False},
            'responsible': {'required': False},
        }