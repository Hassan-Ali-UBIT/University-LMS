from rest_framework import serializers

from .models import AttendanceRecord

from users.serializers import UserSerializer
from content.serializers import LessonSerializer

class AttendanceRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for AttendanceRecord model.
    """
    class Meta:
        model = AttendanceRecord
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "student": {
                "required": False,
            },
            "watch_percentage": {
                "required": False,
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["student"] = UserSerializer(instance.student).data
        representation["lesson"] = LessonSerializer(instance.lesson).data

        return representation




