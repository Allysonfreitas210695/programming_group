from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User

class Group(BaseModel):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='standard_groups_created')
    members = models.ManyToManyField(User, related_name='standard_groups_joined')

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name

