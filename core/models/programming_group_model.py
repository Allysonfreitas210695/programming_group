import hashlib
import os
from django.db import models # type: ignore
from core.models.base_model import BaseModel
from core.models.user_model import User
from core.validators.ProgrammingGroup_validator import validate_difficulty

def get_hashed_filename(instance, filename):
    hash_obj = hashlib.md5()
    hash_obj.update(filename.encode('utf-8'))
    hash_name = hash_obj.hexdigest()
    ext = os.path.splitext(filename)[1] 
    return f'{hash_name}{ext}'

class ProgrammingGroup(BaseModel):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    field_of_interest = models.CharField(max_length=255)
    technologies_used = models.TextField()
    difficulty_level = models.PositiveIntegerField(validators=[validate_difficulty])
    image = models.ImageField(upload_to=get_hashed_filename, blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='programming_groups_created')
    participants = models.ManyToManyField(User, related_name='programming_groups_joined', blank=True)
    
    # Novos campos
    is_recruiting = models.BooleanField(default=False)  # Indica se o grupo está recrutando novos membros
    participants_needed = models.CharField(max_length=255, blank=True, null=True)  # Ex: "Frontend, Backend, DevOps"
    
    class Meta:
        verbose_name = "ProgrammingGroup"
        verbose_name_plural = "ProgrammingGroups"

    def __str__(self):
        return self.title
