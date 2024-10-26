from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models.user_model import User
from core.serializers.contribution_serializer import ContributionSerializer
from core.models.contribution_model import Contribution
from rest_framework.pagination import LimitOffsetPagination
from core.services.contribution_service import ContributionService
from core.shared.customAPIException import CustomAPIException
from rest_framework.permissions import IsAuthenticated

class ContributionPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class ContributionViewSet(viewsets.ViewSet):
    pagination_class = ContributionPagination
    serializer_class = ContributionSerializer

    def list(self, request):
        contributions = ContributionService.list_all_contributions()
        paginator = self.pagination_class()
        paginated_contributions = paginator.paginate_queryset(contributions, request)
        serializer = ContributionSerializer(paginated_contributions, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            contribution = ContributionService.retrieve_contribution(pk)
            serializer = ContributionSerializer(contribution)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def create(self, request):
        user_id = request.data.get("user")
        serializer = ContributionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_instance = User.objects.get(id=user_id)  
                contribution_data = serializer.validated_data
                contribution = ContributionService.create_contribution(user_instance, contribution_data)  
                return Response(ContributionSerializer(contribution).data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = ContributionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                contribution_data = serializer.validated_data
                contribution = ContributionService.update_contribution(pk, contribution_data)
                return Response(ContributionSerializer(contribution).data, status=status.HTTP_200_OK)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            ContributionService.delete_contribution(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    @action(detail=True, methods=['get'])
    def score_user(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            total_score = ContributionService.get_user_total_score(user)
            return Response({"user_id": user.id, "total_score": total_score}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)