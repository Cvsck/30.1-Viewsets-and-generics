import logging
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

logger = logging.getLogger(__name__)


@shared_task
def deactivate_inactive_users():
    from users.models import (
        User,
    )  # РёРјРїРѕСЂС‚ РІРЅСѓС‚СЂРё С„СѓРЅРєС†РёРё вЂ” РґР»СЏ РёР·Р±РµР¶Р°РЅРёСЏ С†РёРєР»РѕРІ

    threshold = now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=threshold, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.warning(f"вњ… Р”РµР°РєС‚РёРІРёСЂРѕРІР°РЅ: {user.email}")
