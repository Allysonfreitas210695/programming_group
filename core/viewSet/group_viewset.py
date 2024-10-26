from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from core.services.group_service import GroupService
from core.serializers.group_serializer import GroupSerializer
from core.shared.customAPIException import CustomAPIException
from rest_framework.pagination import LimitOffsetPagination

class GroupPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class GroupViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    pagination_class = GroupPagination

    def list(self, request):
        user = request.user
        groups = GroupService.list_groups(user)
        paginator = self.pagination_class()
        paginated_groups = paginator.paginate_queryset(groups, request)
        serializer = GroupSerializer(paginated_groups, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            group = GroupService.get_group(pk)
            serializer = GroupSerializer(group)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def create(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                group_data = serializer.validated_data
                group = GroupService.create_group(**group_data)
                return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = GroupSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                group_data = serializer.validated_data
                group = GroupService.update_group(pk, **group_data)
                return Response(GroupSerializer(group).data, status=status.HTTP_200_OK)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            GroupService.delete_group(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
