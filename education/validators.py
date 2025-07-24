from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    if not value.startswith("https://www.youtube.com") and not value.startswith(
        "https://youtu.be"
    ):
        raise ValidationError("Можно использовать только ссылки на youtube.com")
