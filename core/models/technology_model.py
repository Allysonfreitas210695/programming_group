from django.db import models
from core.models.base_model import BaseModel

class Technology(BaseModel):
    LEVEL_CHOICES = [
        ('beginner', 'Iniciante'),
        ('intermediate', 'Intermediário'),
        ('advanced', 'Avançado'),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)  # Nome da tecnologia
    level = models.CharField(max_length=12, choices=LEVEL_CHOICES, null=False, blank=False)  # Nível de conhecimento como escolha

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"

    def __str__(self):
        return f'{self.name} ({self.get_level_display()})'