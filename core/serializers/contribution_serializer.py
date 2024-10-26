from rest_framework import serializers

from core.models.contribution_model import Contribution

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['id', 'user', 'type', 'description', 'score']
        read_only_fields = ['created_at']
