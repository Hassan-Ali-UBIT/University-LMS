from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseDetailAPIView,
    CourseEnrollmentAPIView,
    CourseLessonAPIView,
)

urlpatterns = [
    path("<str:course_id>/lessons/", CourseLessonAPIView.as_view()),
    path("<str:course_id>/students/", CourseEnrollmentAPIView.as_view()),
    path("<str:course_id>/", CourseDetailAPIView.as_view()),
]
