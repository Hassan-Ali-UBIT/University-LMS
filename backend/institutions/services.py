import secrets

from .models import (
    Institution,
)

class InstituitionService:

    @staticmethod
    def generate_unique_code(model, field_name='code', length=8):
        while True:
            code = secrets.token_urlsafe(length)[:length]
            if not model.objects.filter(**{field_name: code}).exists():
                return code


