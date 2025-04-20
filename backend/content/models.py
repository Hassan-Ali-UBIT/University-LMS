import uuid
from django.db import models

from courses.models import Course
from users.models import User


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course,
                                on_delete=models.CASCADE,
                                related_name="lessons"
                                )
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_duration = models.PositiveIntegerField()  # Duration in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LessonMaterial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson,
                                on_delete=models.CASCADE,
                                related_name="materials"
                                )
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson,
                                on_delete=models.CASCADE,
                                related_name="comments"
                                )
    user = models.ForeignKey(User,
                            on_delete=models.CASCADE
                            )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                related_name="replies"
                                )
    user = models.ForeignKey(User,
                            on_delete=models.CASCADE
                            )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
