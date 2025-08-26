import logging
from datetime import UTC, datetime

from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def sample_task():
    logger.info("рџЋЇ Celery is working!")


@shared_task
def beat_task():
    now = datetime.now(UTC)
    logger.warning(f"рџ“… Beat task executed at {now.isoformat()}")


@shared_task
def notify_subscribers(course_id):
    from education.models import Course, Subscription

    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    for subscriber in subscribers:
        send_mail(
            subject=f"РћР±РЅРѕРІР»РµРЅРёРµ РєСѓСЂСЃР°: {course.title}",
            message="РљСѓСЂСЃ Р±С‹Р» РѕР±РЅРѕРІР»С‘РЅ. РџСЂРѕРІРµСЂСЊС‚Рµ РЅРѕРІС‹Рµ РјР°С‚РµСЂРёР°Р»С‹!",
            from_email="noreply@yourdomain.com",
            recipient_list=[subscriber.user.email],
        )
        logger.info(
            f"рџ“Ё Email sent to: {subscriber.user.email} for course: {course.title}"
        )
