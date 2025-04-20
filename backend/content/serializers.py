from rest_framework import serializers

from common.debug import print_parameters
from common.user_exception import validate_file_size
from common.utils import time_to_seconds

from .models import (
    Lesson, LessonMaterial, Comment, Reply,
    WatchSession, WatchSegment
)

from .services import (
    WatchSessionService,
    WatchSegmentService,
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
    
    materials = serializers.ListField(
                    child=serializers.FileField(
                        allow_empty_file=False,
                        required=True,
                        write_only=True,
                        validators=[validate_file_size]
                    ),
                    required=False,
                    write_only=True
                )

    class Meta:
        model = LessonMaterial
        fields = "__all__"
        extra_kwargs = {
            "lesson": {
                "required": False,
                "write_only": True,
            },
            "file_name": {
                "required": False,
            },
            "file_url": {
                "required": False,
            },
            "file_type": {
                "required": False,
            }
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "lesson": {
                "required": False,
                "write_only": True,
            }
        }

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"
        extra_kwargs = {
            "comment": {
                "required": False,
                "write_only": True,
            }
        }

class WatchSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchSession
        fields = "__all__"
        extra_kwargs = {
            "lesson": {
                "required": False,
                "write_only": True,
            },
            "student": {
                "required": False,
                "write_only": True,
            },
            "watched_duration": {
                "read_only": True,
            },
            "last_position": {
                "read_only": True,
            },
        }

class WatchSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchSegment
        fields = "__all__"
        extra_kwargs = {
            "watch_session": {
                "required": False,
                "write_only": True,
            }
        }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        start_position = validated_data.get("start_position")
        end_position = validated_data.get("end_position")

        start_position_seconds = time_to_seconds(start_position)
        end_position_seconds = time_to_seconds(end_position)  

        segment_duration = end_position_seconds - start_position_seconds

        if start_position >= end_position:
            raise serializers.ValidationError("Start position must be less than end position.")
        
        if segment_duration > 30:
            raise serializers.ValidationError("Segment duration cannot exceed 30 seconds.")

        return validated_data







