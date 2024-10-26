from django.test import TestCase
from core.models.group_model import Group
from core.models.user_model import User
from core.services.chat_service import ChatService
from core.shared.customAPIException import CustomAPIException

class ChatServiceTestCase(TestCase):
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

    def test_send_group_chat_message(self):
        message = ChatService.send_group_chat_message(
            group=self.group,
            sender=self.sender,
            message='Hello Group!'
        )
        self.assertEqual(message.message, 'Hello Group!')
        self.assertEqual(message.group, self.group)
        self.assertEqual(message.sender, self.sender)

    def test_send_group_chat_message_not_member(self):
      new_user = User.objects.create(
          email='newuser@test.com',
          password='password123',
          name='New User',
          cpf='33333333333',
          dateOfBirth='1985-01-01'
      )
      with self.assertRaises(CustomAPIException) as context:
          ChatService.send_group_chat_message(
              group=self.group,
              sender=new_user,
              message='Hello Group!'
          )
      self.assertEqual(context.exception.detail, {'error': 'User is not a member of the group'})

    def test_list_group_chat_messages(self):
        ChatService.send_group_chat_message(
            group=self.group,
            sender=self.sender,
            message='Hello Group!'
        )
        messages = ChatService.list_group_chat_messages(self.group)
        self.assertEqual(messages.count(), 1)
        self.assertEqual(messages.first().message, 'Hello Group!')

    def test_send_private_chat_message(self):
        message = ChatService.send_private_chat_message(
            sender=self.sender,
            receiver=self.receiver,
            message='Hello there!'
        )
        self.assertEqual(message.message, 'Hello there!')
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)

    def test_list_private_chat_messages(self):
        ChatService.send_private_chat_message(
            sender=self.sender,
            receiver=self.receiver,
            message='Hello there!'
        )
        messages = ChatService.list_private_chat_messages(self.sender, self.receiver)
        self.assertEqual(messages.count(), 1)
        self.assertEqual(messages.first().message, 'Hello there!')
