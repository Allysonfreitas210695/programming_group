from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User

class Notification(BaseModel):
    NOTIFICATION_TYPE_CHOICES = [
        ('friend_request', 'Friend Request'),
        ('group_invite', 'Group Invite'),
        ('group_update', 'Group Update'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_notifications")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notification for {self.user} - {self.notification_type}"
