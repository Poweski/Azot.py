from django.core.exceptions import ValidationError
from apps.exceptions import WrongPasswordError


def validate_password(password: str):

    if len(password) < 8:
        raise WrongPasswordError('Password must be at least 8 characters long')

    if not any(char.isdigit() for char in password):
        raise WrongPasswordError('Password must contain at least one digit')

    if not any(char.isupper() for char in password):
        raise WrongPasswordError('Password must contain at least one uppercase letter')

    if not any(char.islower() for char in password):
        raise WrongPasswordError('Password must contain at least one lowercase letter')
