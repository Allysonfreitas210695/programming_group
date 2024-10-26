from django.db import models
from .base_model import BaseModel

class FeedPost(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    group = models.ForeignKey('ProgrammingGroup', on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    interest_area = models.ManyToManyField('Interest')
    difficulty_level = models.IntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')])

    def __str__(self):
        return self.title