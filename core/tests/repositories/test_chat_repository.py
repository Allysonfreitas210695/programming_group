from django.test import TestCase
from core.models.group_model import Group
from core.models.user_model import User
from core.models.group_chat_message_model import GroupChatMessage
from core.models.private_chat_message_model import PrivateChatMessage
from core.repositories.chat_repository import ChatRepository

class ChatRepositoryTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create(
            email='sender@test.com',
            password='password123',
            name='Sender',
            cpf='11111111111',
            dateOfBirth='1980-01-01'
        )
        self.receiver = User.objects.create(
            email='receiver@test.com',
            password='password123',
            name='Receiver',
            cpf='22222222222',
            dateOfBirth='1980-01-01'
        )
        self.group = Group.objects.create(
            name='Test Group',
            creator=self.sender
        )
        self.group.members.add(self.sender, self.receiver)

    def test_create_group_chat_message(self):
        message = ChatRepository.create_group_chat_message(
            group=self.group,
            sender=self.sender,
            message='Hello Group!'
        )
        self.assertEqual(message.message, 'Hello Group!')
        self.assertEqual(message.group, self.group)
        self.assertEqual(message.sender, self.sender)

    def test_list_group_chat_messages(self):
        ChatRepository.create_group_chat_message(
            group=self.group,
            sender=self.sender,
            message='Hello Group!'
        )
        messages = ChatRepository.list_group_chat_messages(self.group)
        self.assertEqual(messages.count(), 1)
        self.assertEqual(messages.first().message, 'Hello Group!')

    def test_create_private_chat_message(self):
        message = ChatRepository.create_private_chat_message(
            sender=self.sender,
            receiver=self.receiver,
            message='Hello there!'
        )
        self.assertEqual(message.message, 'Hello there!')
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)

    def test_list_private_chat_messages(self):
        ChatRepository.create_private_chat_message(
            sender=self.sender,
            receiver=self.receiver,
            message='Hello there!'
        )
        messages = ChatRepository.list_private_chat_messages(self.sender, self.receiver)
        self.assertEqual(messages.count(), 1)
        self.assertEqual(messages.first().message, 'Hello there!')
