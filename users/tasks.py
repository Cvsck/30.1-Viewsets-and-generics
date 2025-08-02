import logging
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

logger = logging.getLogger(__name__)


@shared_task
def deactivate_inactive_users():
    from users.models import \
        User  # импорт внутри функции — для избежания циклов

    threshold = now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=threshold, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.warning(f"✅ Деактивирован: {user.email}")
