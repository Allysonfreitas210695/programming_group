from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from core.serializers.interest_serializer import InterestSerializer
from core.services.interest_service import InterestService
from core.shared.customAPIException import CustomAPIException
from rest_framework.response import Response
from rest_framework import status

class InterestViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InterestSerializer

    def list(self, request):
        try:
            interests = InterestService.list_all_interests()
            serializer = InterestSerializer(interests, many=True)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def retrieve(self, request, pk=None):
        try:
            interest = InterestService.retrieve_interest(pk)
            serializer = InterestSerializer(interest)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def create(self, request):
        serializer = InterestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                interest = InterestService.create_interest(serializer.validated_data)
                response_serializer = InterestSerializer(interest)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({'detail': str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            interest = InterestService.retrieve_interest(pk)
            serializer = InterestSerializer(interest, data=request.data, partial=True)
            if serializer.is_valid():
                updated_interest = InterestService.update_interest(pk, serializer.validated_data)
                response_serializer = InterestSerializer(updated_interest)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)

    def destroy(self, request, pk=None):
        try:
            InterestService.delete_interest(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({'detail': str(e)}, status=e.status_code)
