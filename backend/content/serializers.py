from rest_framework import serializers

from .models import (
    Lesson, LessonMaterial,
    Comment, Reply
)

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            "course": {
                "required": False,
                "write_only": True,
            }
        }

class LessonMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonMaterial
        fields = "__all__"



