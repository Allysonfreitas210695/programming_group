from core.models.group_chat_message_model import GroupChatMessage
from core.models.private_chat_message_model import PrivateChatMessage
from core.models.user_model import User

class ChatRepository:

    @staticmethod
    def list_group_chat_messages(group):
        return GroupChatMessage.objects.filter(group=group).order_by('created_at')

    @staticmethod
    def create_group_chat_message(group, sender, message):
        if not isinstance(sender, User):
            raise ValueError("The sender must be an instance of User")
        return GroupChatMessage.objects.create(group=group, sender=sender, message=message)

    @staticmethod
    def list_private_chat_messages(sender, receiver):
        return PrivateChatMessage.objects.filter(sender=sender, receiver=receiver).order_by('created_at')

    @staticmethod
    def create_private_chat_message(sender, receiver, message):
        if not isinstance(sender, User) or not isinstance(receiver, User):
            raise ValueError("Both sender and receiver must be instances of User")
        return PrivateChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
