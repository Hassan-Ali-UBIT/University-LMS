from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from institutions.permissions import (
    IsInstitutionAdmin,
    IsInstitutionAdminOfCourse
)

from content.serializers import (
    LessonSerializer,
)

from .models import (
    Course,
    CourseEnrollment
)

from .serializers import (
    CourseSerializer,
    CourseEnrollmentSerializer
)

from .permissions import (
    IsCourseOwner
)

from .services import (
    CourseService
)

class CourseDetailAPIView(APIView):
    permission_classes = [(IsCourseOwner | IsInstitutionAdminOfCourse)]
    def get(self, request, *args, **kwargs):

        course_id = kwargs.get("course_id")

        course_instance = get_object_or_404(Course, id=course_id)

        course_serializer = CourseSerializer(course_instance)

        return Response({"data": course_serializer.data})
    
    def put(self, request, *args, **kwargs):

        course_id = kwargs.get("course_id")

        course_instance = get_object_or_404(Course, id=course_id)

        self.check_object_permissions(request, course_instance)

        course_serializer = CourseSerializer(course_instance, data=request.data)

        course_serializer.is_valid(raise_exception=True)

        course_serializer.save()

        return Response({"data": course_serializer.data})
    
    def delete(self, request, *args, **kwargs):

        course_id = kwargs.get("course_id")

        course_instance = get_object_or_404(Course, id=course_id)

        self.check_object_permissions(request, course_instance)

        course_instance.delete()

        return Response({"message": "course deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class CourseEnrollmentAPIView(APIView):

    def get(self, request, *args, **kwargs):

        course_id = kwargs.get("course_id")

        course_students = CourseEnrollment.objects.filter(course=course_id)

        course_enrollment_serializer = CourseEnrollmentSerializer(course_students, many=True)

        return Response({"data": course_enrollment_serializer.data})
    
    def post(self, request, *args, **kwargs):

        course_id = kwargs.get("course_id")

        course = get_object_or_404(Course, id=course_id)

        course_enrollment_serializer = CourseEnrollmentSerializer(data=request.data)

        course_enrollment_serializer.is_valid(raise_exception=True)

        student = course_enrollment_serializer.validated_data["student"]

        CourseService.validate_member_not_exists_in_course(course, student)

        CourseService.check_student_add_permission(course, request.user)

        course_enrollment_serializer.save(course=course)

        return Response({"data": "student enrolled successfully"}, status=status.HTTP_201_CREATED)

class CourseLessonAPIView(APIView):
    permission_classes = [IsCourseOwner]
    
    def get(self, request, *args, **kwargs):

        course_id = kwargs.get("course_id")

        course_instance = get_object_or_404(Course, id=course_id)

        lessons = course_instance.lessons.all()

        lessons_serializer = LessonSerializer(lessons, many=True)

        return Response({"data": lessons_serializer.data})
    
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")

        course_instance = get_object_or_404(Course, id=course_id)

        self.check_object_permissions(request, course_instance)

        lesson_serializer = LessonSerializer(data=request.data)

        lesson_serializer.is_valid(raise_exception=True)

        lesson_serializer.save(course=course_instance)

        return Response({"data": lesson_serializer.data}, status=status.HTTP_201_CREATED)
    

