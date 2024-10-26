from rest_framework import serializers
from core.models.contribution_model import Contribution
from core.models.profile_model import UserProfile
from core.serializers.contribution_serializer import ContributionSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    contributions = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'total_score', 'contributions']

    def get_contributions(self, obj):
        contributions = Contribution.objects.filter(user=obj.user)
        return ContributionSerializer(contributions, many=True).data
