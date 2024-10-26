from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.serializers.private_chat_message_serializer import PrivateChatMessageSerializer
from core.services.chat_service import ChatService
from core.services.user_services import UserService
from core.shared.customAPIException import CustomAPIException

class PrivateChatViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateChatMessageSerializer

    def list(self, request, user_id):
        try:
            sender = request.user
            receiver = UserService.retrieve_user(user_id)
            messages = ChatService.list_private_chat_messages(sender, receiver)
            serializer = PrivateChatMessageSerializer(messages, many=True)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def create(self, request, user_id):
        try:
            sender = request.user
            receiver = UserService.retrieve_user(user_id)
            message = request.data.get('message')

            if not message:
                return Response({"detail": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

            new_message = ChatService.send_private_chat_message(sender, receiver, message)
            serializer = PrivateChatMessageSerializer(new_message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
