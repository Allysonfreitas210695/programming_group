from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def seed_universities(sender, **kwargs):
    if sender.name == 'core': 
        call_command('seed_universities')

@receiver(post_migrate)
def seed_technologies(sender, **kwargs):
    if sender.name == 'core': 
        call_command('seed_technologies')

@receiver(post_migrate)
def seed_interests(sender, **kwargs):
    if sender.name == 'core': 
        call_command('seed_interests')