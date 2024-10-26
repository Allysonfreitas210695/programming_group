from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User

class PrivateChatMessage(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()

    def __str__(self):
        return f"Private message from {self.sender} to {self.receiver}"
