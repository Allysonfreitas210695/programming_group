from django.core.management.base import BaseCommand
from core.models.interest_model import Interest

class Command(BaseCommand):
    help = 'Seed the interests table with data'

    def handle(self, *args, **kwargs):
        interests = [
            {'name': 'App Mobile'},
            {'name': 'WebApp'},
            {'name': 'Banco de Dados'},
            {'name': 'Programação Backend'},
            {'name': 'Programação Frontend'},
            {'name': 'DevOps'},
            {'name': 'Machine Learning'},
            {'name': 'Inteligência Artificial'},
            {'name': 'Cloud Computing'},
            {'name': 'Segurança da Informação'},
            {'name': 'Data Science'},
            {'name': 'IoT (Internet of Things)'},
            {'name': 'Games'},
            {'name': 'Blockchain'},
            {'name': 'Realidade Virtual'},
            {'name': 'Realidade Aumentada'},
        ]

        for interest in interests:
            existing_interest = Interest.objects.filter(name=interest['name']).first()
            if not existing_interest:
                Interest.objects.create(**interest)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the interests table.'))
