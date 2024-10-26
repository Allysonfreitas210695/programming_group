from django.db import models
from core.models.base_model import BaseModel
from core.models.group_model import Group
from core.models.user_model import User

class GroupChatMessage(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        verbose_name = "GroupChatMessage"
        verbose_name_plural = "GroupChatMessages"

    def __str__(self):
        return f"Message in {self.group} by {self.sender}"
