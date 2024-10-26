from rest_framework import serializers
from core.models.programming_group_model import ProgrammingGroup

class ProgrammingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingGroup
        fields = ['id', 'title', 'description', 'field_of_interest', 'technologies_used', 'difficulty_level', 'image', 'privacy', 'status', 'creator', 'participants', 'is_recruiting', 'participants_needed']
        extra_kwargs = {
            'participants': {'required': False},
            'is_recruiting': {'required': False},
            'participants_needed': {'required': False},
        }
