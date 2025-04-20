import uuid
from django.db import models

from institutions.models import Institution
from users.models import User


class Course(models.Model):
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    institution = models.ForeignKey(Institution,
                                    on_delete=models.CASCADE,
                                    related_name="courses"
                                    )
    teacher = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="taught_courses"
                                )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    min_attendance_percent = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CourseEnrollment(models.Model):
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    course = models.ForeignKey(Course,
                                on_delete=models.CASCADE,
                                related_name="enrollments")
    student = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="enrolled_courses"
                                )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "student")
