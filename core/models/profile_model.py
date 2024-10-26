from django.db import models
from core.models.base_model import BaseModel
from core.models.user_model import User
from core.models.technology_model import Technology
from core.models.interest_model import Interest

class UserProfile(BaseModel):
    PRIVACY_CHOICES = [
        ('public', 'Público'),
        ('private', 'Privado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  
    technologies = models.ManyToManyField(Technology, blank=True, related_name='profiles')  
    interests = models.ManyToManyField(Interest, blank=True, related_name='profiles')  
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES, default='public') 

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return f'Perfil de {self.user.username}'
