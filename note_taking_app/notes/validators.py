from django.core.exceptions import ValidationError

def validate_no_xss(value):
    if '<script>' in value:
        raise ValidationError('XSS attack detected!')