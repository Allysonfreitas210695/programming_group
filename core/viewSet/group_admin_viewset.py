from uuid import UUID
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from core.services.group_admin_service import GroupAdminService
from core.models.group_model import Group
from core.models.user_model import User
from core.serializers.group_admin_serializer import AddAdminSerializer, GroupAdminSerializer, RemoveAdminSerializer
from core.shared.customAPIException import CustomAPIException

class GroupAdminViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AddAdminSerializer,
        responses={
            201: OpenApiResponse(description='Admin added successfully'),
            400: OpenApiResponse(description='Bad request'),
            404: OpenApiResponse(description='Group or User not found')
        },
        parameters=[
            OpenApiParameter(name='id', type=UUID, description='Group ID', location=OpenApiParameter.PATH)
        ],
        tags=['Group Admins'],
    )

    @action(detail=True, methods=['post'], url_path='add')
    def add_admin(self, request, pk=None):
        serializer = AddAdminSerializer(data=request.data)
        if serializer.is_valid():
            group_id = serializer.validated_data['group_id']
            user_id = serializer.validated_data['user_id']
            try:
                group = Group.objects.get(id=group_id)
                user = User.objects.get(id=user_id)
                GroupAdminService.add_admin(group, user)
                return Response(status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
            except Group.DoesNotExist:
                return Response({"detail": 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RemoveAdminSerializer,
        responses={
            204: OpenApiResponse(description='Admin removed successfully'),
            400: OpenApiResponse(description='Bad request'),
            404: OpenApiResponse(description='Group or User not found')
        },
        parameters=[
            OpenApiParameter(name='id', type=UUID, description='Group ID', location=OpenApiParameter.PATH)
        ],
        tags=['Group Admins'],
    )
    
    @action(detail=True, methods=['post'], url_path='remove')
    def remove_admin(self, request, pk=None):
        serializer = RemoveAdminSerializer(data=request.data)
        if serializer.is_valid():
            group_id = serializer.validated_data['group_id']
            user_id = serializer.validated_data['user_id']
            try:
                group = Group.objects.get(id=group_id)
                user = User.objects.get(id=user_id)
                GroupAdminService.remove_admin(group, user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
            except Group.DoesNotExist:
                return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            200: GroupAdminSerializer(many=True),
            404: OpenApiResponse(description='Group not found')
        },
        parameters=[
            OpenApiParameter(name='id', type=UUID, description='Group ID', location=OpenApiParameter.PATH)
        ],
        tags=['Group Admins'],
    )
    @action(detail=True, methods=['get'], url_path='admins')
    def list_admins(self, request, pk=None):
        try:
            group = Group.objects.get(id=pk)
            admins = GroupAdminService.list_admins(group)
            serializer = GroupAdminSerializer(admins, many=True)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
