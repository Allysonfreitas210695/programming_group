from rest_framework import serializers
from core.models.profile_model import UserProfile
from core.models.interest_model import Interest
from core.models.technology_model import Technology
from core.models.user_model import User

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Permitir enviar o ID do usuário
    technologies = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Technology.objects.all(), 
        required=False, 
        allow_null=True
    )
    interests = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Interest.objects.all(), 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'photo', 'description', 'rating', 'technologies', 'interests', 'privacy']
        extra_kwargs = {
            'technologies': {'required': False, 'allow_null': True},
            'interests': {'required': False, 'allow_null': True},
            'photo': {'required': False},
        }
