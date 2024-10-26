from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from core.serializers.notification_serializer import NotificationSerializer
from core.models.notification_model import Notification
from rest_framework.pagination import LimitOffsetPagination
from core.services.notification_service import NotificationService
from core.shared.customAPIException import CustomAPIException

class NotificationPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class NotificationViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def list(self, request):
        user = request.user 
        notifications = NotificationService.list_all_notifications(user)
        paginator = self.pagination_class()
        paginated_notifications = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(paginated_notifications, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            notification = NotificationService.retrieve_notification(pk)
            serializer = NotificationSerializer(notification)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def create(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                notification_data = serializer.validated_data
                notification = NotificationService.create_notification(notification_data)
                return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                notification_data = serializer.validated_data
                notification = NotificationService.update_notification(pk, notification_data)
                return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)
            except CustomAPIException as e:
                return Response({"detail": str(e)}, status=e.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            NotificationService.delete_notification(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
