# comment_model.py
from django.db import models # type: ignore
from core.models.base_model import BaseModel
from core.models.user_model import User
from core.models.task_model import Task  # Certifique-se de que o caminho está correto

class TaskComment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_created')
    content = models.TextField()
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    
    def __str__(self):
        return f'Comment by {self.author} on {self.task.title}'
