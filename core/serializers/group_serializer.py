from rest_framework import serializers
from core.models.group_model import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'creator', 'members']
