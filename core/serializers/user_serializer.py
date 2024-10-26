from rest_framework import serializers
from core.models.university_model import University
from core.models.user_model import User

class UserSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all(), required=False, allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'cpf', 'email', 'dateOfBirth', 'status', 'password', 'university']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.setdefault('university', None)
        validated_data.setdefault('is_active', True)
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.email = validated_data.get('email', instance.email)
        instance.dateOfBirth = validated_data.get('dateOfBirth', instance.dateOfBirth)
        instance.status = validated_data.get('status', instance.status)

        instance.university = validated_data.get('university', None)
        
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
