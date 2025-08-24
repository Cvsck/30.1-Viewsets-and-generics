from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_courses",
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    description = models.TextField()
    video_url = models.URLField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_lessons",  # С‚РѕР¶Рµ СѓРЅРёРєР°Р»СЊРЅРѕРµ
    )

    def __str__(self):
        return f"{self.title} ({self.course.title})"


# education/models.py


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")
