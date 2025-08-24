from django.core.exceptions import ValidationError


class VideoURLValidator:
    def __call__(self, value):
        if not (
            value.startswith("https://www.youtube.com")
            or value.startswith("https://youtu.be")
        ):
            raise ValidationError(
                "РњРѕР¶РЅРѕ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ С‚РѕР»СЊРєРѕ СЃСЃС‹Р»РєРё РЅР° youtube.com"
            )
