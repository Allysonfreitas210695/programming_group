# task_model.py
import hashlib
import os
from django.db import models # type: ignore
from core.models.base_model import BaseModel
from core.models.user_model import User
from core.models.programming_group_model import ProgrammingGroup  
from core.validators.task_validator import validate_deadline, validate_attachment_type, validate_responsible_users_in_group

def get_hashed_filename(instance, filename):
    hash_obj = hashlib.md5()
    hash_obj.update(filename.encode('utf-8'))
    hash_name = hash_obj.hexdigest()
    ext = os.path.splitext(filename)[1]
    return f'{hash_name}{ext}'

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    attachments = models.FileField(upload_to=get_hashed_filename, blank=True, null=True, validators=[validate_attachment_type])  
    deadline = models.DateTimeField(validators=[validate_deadline])  
    group = models.ForeignKey(ProgrammingGroup, on_delete=models.CASCADE, related_name='tasks')
    responsible = models.ManyToManyField(User, related_name='tasks_responsible')
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def clean(self):
        validate_responsible_users_in_group(self.responsible.all(), self.group)

    def __str__(self):
        return self.title
