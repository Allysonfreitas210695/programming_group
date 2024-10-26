from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from core.services.university_services import UniversityService
from core.serializers.university_serializer import UniversitySerializer
from core.shared.customAPIException import CustomAPIException

class UniversityPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class UniversityViewSet(viewsets.ViewSet):
    serializer_class = UniversitySerializer
    pagination_class = UniversityPagination

    def list(self, request):
        universities = UniversityService.list_all_universities()
        paginator = self.pagination_class()
        paginated_universities = paginator.paginate_queryset(universities, request)
        serializer = UniversitySerializer(paginated_universities, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            university = UniversityService.retrieve_university(pk)
            serializer = UniversitySerializer(university)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def create(self, request):
        serializer = UniversitySerializer(data=request.data)
        if serializer.is_valid():
            try:
                university_data = serializer.validated_data
                university = UniversityService.create_university(university_data)
                return Response(UniversitySerializer(university).data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = UniversitySerializer(data=request.data)
        if serializer.is_valid():
            try:
                university_data = serializer.validated_data
                university = UniversityService.update_university(pk, university_data)
                return Response(UniversitySerializer(university).data, status=status.HTTP_200_OK)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            UniversityService.delete_university(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
