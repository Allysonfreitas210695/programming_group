from django.core.exceptions import ValidationError

def validate_difficulty(value):
    if value < 1 or value > 5:
        raise ValidationError('Difficulty level must be between 1 and 5.')
