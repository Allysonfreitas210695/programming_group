from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from core.serializers.programming_group_serializer import ProgrammingGroupSerializer
from core.services.programming_group_service import ProgrammingGroupService
from core.shared.customAPIException import CustomAPIException
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status

class ProgrammingGroupPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class ProgrammingGroupViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProgrammingGroupSerializer
    pagination_class = ProgrammingGroupPagination
    
    def list(self, request):
        try:
            paginator = self.pagination_class()
            groups = ProgrammingGroupService.list_all_groups()
            page = paginator.paginate_queryset(groups, request)
            serializer = ProgrammingGroupSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def retrieve(self, request, pk=None):
        try:
            group = ProgrammingGroupService.retrieve_group(pk)
            serializer = ProgrammingGroupSerializer(group)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def create(self, request):
        serializer = ProgrammingGroupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                group = ProgrammingGroupService.create_group(serializer.validated_data)
                return Response(ProgrammingGroupSerializer(group).data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({'detail': str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            group = ProgrammingGroupService.retrieve_group(pk)
            serializer = ProgrammingGroupSerializer(group, data=request.data, partial=True)
            if serializer.is_valid():
                group = ProgrammingGroupService.update_group(pk, serializer.validated_data)
                return Response(ProgrammingGroupSerializer(group).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def destroy(self, request, pk=None):
        try:
            ProgrammingGroupService.delete_group(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)
