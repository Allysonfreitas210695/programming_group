from django.db import models
from core.models.base_model import BaseModel
from core.models.group_model import Group
from core.models.user_model import User


class GroupAdmin(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='admins')
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('group', 'admin')
    
    def __str__(self):
        return f"{self.admin} - Admin of {self.group}"
