from rest_framework import serializers
from core.models.technology_model import Technology

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'level']
