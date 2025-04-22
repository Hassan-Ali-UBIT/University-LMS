from rest_framework import serializers

from users.models import User, Role
from users.serializers import (
    UserSerializer, RoleSerializer
)

from institutions.serializers import (
    InstitutionSerializer
)

from .models import (
    Course, CourseEnrollment
)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["institution", "teacher", "created_at", "updated_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["institution"] = InstitutionSerializer(instance.institution).data
        representation["teacher"] = UserSerializer(instance.teacher).data
        
        return representation
    
class CourseEnrollmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseEnrollment
        fields = "__all__"
        read_only_fields = ['course']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.pop("course", None)
        representation["student"] = UserSerializer(instance.student).data

        return representation
    

