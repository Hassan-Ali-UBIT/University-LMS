from django.urls import path

from .views import (
    StudentAttendanceAPIView,
)

urlpatterns = [
    path("<str:student_id>/", StudentAttendanceAPIView.as_view()),
]
