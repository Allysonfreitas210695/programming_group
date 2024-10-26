from core.repositories.chat_repository import ChatRepository
from core.shared.customAPIException import CustomAPIException
from core.models import User

class ChatService:

    @staticmethod
    def list_group_chat_messages(group):
        return ChatRepository.list_group_chat_messages(group)

    @staticmethod
    def send_group_chat_message(group, sender, message):
        if not isinstance(sender, User):
            raise CustomAPIException('Invalid sender user instance', 400)
        if not group.members.filter(id=sender.id).exists():
            raise CustomAPIException('User is not a member of the group', 403)
        return ChatRepository.create_group_chat_message(group, sender, message)

    @staticmethod
    def list_private_chat_messages(sender, receiver):
        if not isinstance(sender, User) or not isinstance(receiver, User):
            raise CustomAPIException('Invalid user instance', 400)
        return ChatRepository.list_private_chat_messages(sender, receiver)

    @staticmethod
    def send_private_chat_message(sender, receiver, message):
        if not isinstance(sender, User) or not isinstance(receiver, User):
            raise CustomAPIException('Invalid user instance', 400)
        return ChatRepository.create_private_chat_message(sender, receiver, message)
