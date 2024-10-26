from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.models.group_model import Group
from core.serializers.group_chat_message_serializer import GroupChatMessageSerializer
from core.services.chat_service import ChatService
from core.services.group_service import GroupService
from core.shared.customAPIException import CustomAPIException

class GroupChatViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GroupChatMessageSerializer

    def list(self, request, group_id):
        try:
            group = GroupService.get_group(group_id)
            messages = ChatService.list_group_chat_messages(group)
            serializer = GroupChatMessageSerializer(messages, many=True)
            return Response(serializer.data)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, group_id):
        try:
            group = GroupService.get_group(group_id) 
            sender = request.user
            message = request.data.get('message')

            if not message:
                return Response({"detail": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

            new_message = ChatService.send_group_chat_message(group, sender, message)
            serializer = GroupChatMessageSerializer(new_message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except CustomAPIException as e:
            return Response({"detail": str(e)}, status=e.status_code)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
