from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from core.serializers.technology_serializer import TechnologySerializer
from core.services.technology_service import TechnologyService
from core.shared.customAPIException import CustomAPIException
from rest_framework.response import Response
from rest_framework import status

class TechnologyViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TechnologySerializer

    def list(self, request):
        try:
            technologies = TechnologyService.list_all_technologies()
            serializer = TechnologySerializer(technologies, many=True)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def retrieve(self, request, pk=None):
        try:
            technology = TechnologyService.retrieve_technology(pk)
            serializer = TechnologySerializer(technology)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def create(self, request):
        serializer = TechnologySerializer(data=request.data)
        if serializer.is_valid():
            try:
                technology = TechnologyService.create_technology(serializer.validated_data)
                response_serializer = TechnologySerializer(technology)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({'detail': str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            technology = TechnologyService.retrieve_technology(pk)
            serializer = TechnologySerializer(technology, data=request.data, partial=True)
            if serializer.is_valid():
                updated_technology = TechnologyService.update_technology(pk, serializer.validated_data)
                response_serializer = TechnologySerializer(updated_technology)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def destroy(self, request, pk=None):
        try:
            TechnologyService.delete_technology(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)
