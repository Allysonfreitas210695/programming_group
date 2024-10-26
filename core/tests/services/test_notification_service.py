from django.test import TestCase
from core.models.notification_model import Notification
from core.models.user_model import User
from core.models.university_model import University
from core.services.notification_service import NotificationService
from core.shared.customAPIException import CustomAPIException

class NotificationServiceTest(TestCase):
    
    def setUp(self):
        self.university = University.objects.create(name='University A')
        self.user = User.objects.create(
            name='John Doe',
            cpf='12345678901',
            email='john.doe@example.com',
            dateOfBirth='1990-01-01',
            status='active',
            university=self.university,
            password='password123'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            sender=self.user,
            notification_type='friend_request',
            message='You have a new friend request.'
        )
    
    def test_list_all_notifications(self):
        notifications = NotificationService.list_all_notifications(self.user)
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().message, self.notification.message)

    def test_retrieve_notification(self):
        notification = NotificationService.retrieve_notification(self.notification.id)
        self.assertEqual(notification.message, self.notification.message)

    def test_create_notification(self):
        notification_data = {
            'user': self.user,
            'sender': self.user,
            'notification_type': 'group_invite',
            'message': 'You have been invited to a group.'
        }
        notification = NotificationService.create_notification(notification_data)
        self.assertEqual(notification.message, notification_data['message'])

    def test_update_notification(self):
        updated_data = {'message': 'Updated notification message.'}
        notification = NotificationService.update_notification(self.notification.id, updated_data)
        self.assertEqual(notification.message, updated_data['message'])

    def test_delete_notification(self):
        NotificationService.delete_notification(self.notification.id)
        with self.assertRaises(CustomAPIException) as context:
            NotificationService.retrieve_notification(self.notification.id)
        self.assertEqual(context.exception.status_code, 404)
