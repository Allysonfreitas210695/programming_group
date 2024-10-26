from django.db import models
from core.models.base_model import BaseModel

class University(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=True)
    city = models.CharField(max_length=255,null=False, blank=True)
    state = models.CharField(max_length=2, null=False, blank=True)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universitys"

    def __str__(self):
        return self.name
