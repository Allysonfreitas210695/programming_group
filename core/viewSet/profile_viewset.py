from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from core.models.profile_model import UserProfile
from core.serializers.profile_serializer import UserProfileSerializer
from core.services.profile_service import UserProfileService
from core.shared.customAPIException import CustomAPIException
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

class UserProfilePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UserProfileViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    pagination_class = UserProfilePagination
    
    def list(self, request):
        try:
            paginator = self.pagination_class()
            profiles = UserProfileService.list_all_profiles()
            page = paginator.paginate_queryset(profiles, request)
            serializer = UserProfileSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def retrieve(self, request, pk=None):
        try:
            profile = UserProfileService.retrieve_profile(pk)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def create(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                # Adiciona o usuário autenticado aos dados validados
                validated_data['user'] = request.user
                
                # Cria o perfil sem os campos Many-to-Many (technologies e interests)
                profile = UserProfile.objects.create(
                    user=validated_data['user'],
                    photo=validated_data.get('photo', None),
                    description=validated_data.get('description', ''),
                    rating=validated_data.get('rating', 0),
                    privacy=validated_data.get('privacy', 'public')
                )

                # Define os campos Many-to-Many depois da criação
                if 'technologies' in validated_data:
                    profile.technologies.set(validated_data['technologies'])
                if 'interests' in validated_data:
                    profile.interests.set(validated_data['interests'])
                
                profile.save()

                # Retorna os dados do perfil criado
                response_serializer = UserProfileSerializer(profile)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            except CustomAPIException as e:
                return Response({'detail': str(e)}, status=e.status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        try:
            # Busca o perfil pelo `id` (pk) ao invés de `user_id`
            profile = UserProfileService.retrieve_profile(pk)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                updated_profile = UserProfileService.update_profile(pk, serializer.validated_data)
                response_serializer = UserProfileSerializer(updated_profile)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)


    def destroy(self, request, pk=None):
        try:
            UserProfileService.delete_profile(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)
