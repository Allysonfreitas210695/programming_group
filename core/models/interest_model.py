from django.db import models
from core.models.base_model import BaseModel

class Interest(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"

    def __str__(self):
        return self.name