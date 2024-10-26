from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_deadline(value):
    if value < timezone.now():
        raise ValidationError('A data limite não pode ser no passado.')

def validate_attachment_type(file):
    valid_mime_types = ['application/pdf', 'image/jpeg', 'image/png']
    if file.content_type not in valid_mime_types:
        raise ValidationError('Tipo de arquivo não suportado. Apenas PDF, JPEG, e PNG são permitidos.')

def validate_responsible_users_in_group(responsibles, group):
    for user in responsibles:
        if user not in group.participants.all():
            raise ValidationError(f'Usuário {user.username} não é um membro do grupo.')