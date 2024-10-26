from django.core.management.base import BaseCommand
from core.models.university_model import University

class Command(BaseCommand):
    help = 'Seed the universities table with data'

    def handle(self, *args, **kwargs):
        universities = [
            {'name': 'Universidade de São Paulo (USP)', 'city': 'São Paulo', 'state': 'SP'},
            {'name': 'Universidade Estadual de Campinas (UNICAMP)', 'city': 'Campinas', 'state': 'SP'},
            {'name': 'Universidade Federal do Rio de Janeiro (UFRJ)', 'city': 'Rio de Janeiro', 'state': 'RJ'},
            {'name': 'Universidade Federal de Minas Gerais (UFMG)', 'city': 'Belo Horizonte', 'state': 'MG'},
            {'name': 'Universidade Federal do Rio Grande do Sul (UFRGS)', 'city': 'Porto Alegre', 'state': 'RS'},
            {'name': 'Universidade Federal de Pernambuco (UFPE)', 'city': 'Recife', 'state': 'PE'},
            {'name': 'Universidade Federal do Ceará (UFC)', 'city': 'Fortaleza', 'state': 'CE'},
            {'name': 'Universidade Federal da Bahia (UFBA)', 'city': 'Salvador', 'state': 'BA'},
            {'name': 'Universidade Federal de Goiás (UFG)', 'city': 'Goiânia', 'state': 'GO'},
            {'name': 'Universidade Federal de São Carlos (UFSCar)', 'city': 'São Carlos', 'state': 'SP'},
            {'name': 'Universidade Federal de Santa Catarina (UFSC)', 'city': 'Florianópolis', 'state': 'SC'},
            {'name': 'Universidade Federal do Pará (UFPA)', 'city': 'Belém', 'state': 'PA'},
            {'name': 'Universidade Federal de Sergipe (UFS)', 'city': 'São Cristóvão', 'state': 'SE'},
            {'name': 'Universidade Federal do Maranhão (UFMA)', 'city': 'São Luís', 'state': 'MA'},
            {'name': 'Universidade Federal do Amazonas (UFAM)', 'city': 'Manaus', 'state': 'AM'},
            {'name': 'Universidade Federal do Piauí (UFPI)', 'city': 'Teresina', 'state': 'PI'},
            {'name': 'Universidade Federal de Lavras (UFLA)', 'city': 'Lavras', 'state': 'MG'},
            {'name': 'Universidade Federal de Viçosa (UFV)', 'city': 'Viçosa', 'state': 'MG'},
            {'name': 'Universidade Federal de Uberlândia (UFU)', 'city': 'Uberlândia', 'state': 'MG'},
            {'name': 'Universidade Federal de Mato Grosso (UFMT)', 'city': 'Cuiabá', 'state': 'MT'},
            {'name': 'Universidade Federal do Tocantins (UFT)', 'city': 'Palmas', 'state': 'TO'},
            {'name': 'Universidade Federal de Rondônia (UNIR)', 'city': 'Porto Velho', 'state': 'RO'},
            {'name': 'Universidade Federal do Acre (UFAC)', 'city': 'Rio Branco', 'state': 'AC'},
            {'name': 'Universidade Federal de Roraima (UFRR)', 'city': 'Boa Vista', 'state': 'RR'},
            {'name': 'Universidade Federal do Amapá (UNIFAP)', 'city': 'Macapá', 'state': 'AP'},
            {'name': 'Universidade Federal de São João del-Rei (UFSJ)', 'city': 'São João del-Rei', 'state': 'MG'},
            {'name': 'Universidade Federal do Espírito Santo (UFES)', 'city': 'Vitória', 'state': 'ES'},
            {'name': 'Universidade Federal de Juiz de Fora (UFJF)', 'city': 'Juiz de Fora', 'state': 'MG'},
            {'name': 'Universidade Federal da Paraíba (UFPB)', 'city': 'João Pessoa', 'state': 'PB'},
            {'name': 'Universidade Federal de Santa Maria (UFSM)', 'city': 'Santa Maria', 'state': 'RS'},
            {'name': 'Universidade Federal de São Paulo (UNIFESP)', 'city': 'São Paulo', 'state': 'SP'},
            {'name': 'Universidade Estadual do Rio de Janeiro (UERJ)', 'city': 'Rio de Janeiro', 'state': 'RJ'},
            {'name': 'Universidade Estadual Paulista (UNESP)', 'city': 'São Paulo', 'state': 'SP'},
            {'name': 'Universidade Federal do Paraná (UFPR)', 'city': 'Curitiba', 'state': 'PR'},
            {'name': 'Universidade Federal de Itajubá (UNIFEI)', 'city': 'Itajubá', 'state': 'MG'},
            {'name': 'Universidade Federal do Semi-Árido (UFERSA)', 'city': 'Mossoró', 'state': 'RN'}
        ]

        for university in universities:
            existing_university = University.objects.filter(name=university['name'], city=university['city'], state=university['state']).first()
            if not existing_university:
                University.objects.create(**university)
