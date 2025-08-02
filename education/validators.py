from django.core.exceptions import ValidationError


class VideoURLValidator:
    def __call__(self, value):
        if not (
            value.startswith("https://www.youtube.com")
            or value.startswith("https://youtu.be")
        ):
            raise ValidationError("Можно использовать только ссылки на youtube.com")
