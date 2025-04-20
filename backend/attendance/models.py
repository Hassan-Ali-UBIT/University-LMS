import uuid
from django.db import models
from content.models import Lesson
from users.models import User

# Create your models here.
class AttendanceRecord(models.Model):
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    lesson = models.ForeignKey(Lesson,
                                on_delete=models.CASCADE,
                                related_name="attendance_records")
    student = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="attendance_records")
    watch_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

