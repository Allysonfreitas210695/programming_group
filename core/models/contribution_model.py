from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User

class Contribution(BaseModel):
    CONTRIBUTION_TYPES = [
        ('project', 'Project'),
        ('article', 'Article'),
        ('code', 'Code Contribution'),
        ('event', 'Event Participation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES)
    description = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Contribution'
        verbose_name_plural = 'Contributions'

    def __str__(self):
        return f'{self.type} - {self.user.name} ({self.score} pontos)'
