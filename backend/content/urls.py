from django.urls import path

from .views import (
    LessonMaterialAPIView,
    LessonAPIView,
    WatchSessionAPIView,
    WatchSegmentAPIView,
    AttendanceRecordAPIView,
)

urlpatterns = [
    path("<str:lesson_id>/attendance/", AttendanceRecordAPIView.as_view()),
    path("<str:lesson_id>/watch-segment/", WatchSegmentAPIView.as_view()),
    path("<str:lesson_id>/watch-session/", WatchSessionAPIView.as_view()),
    path("<str:lesson_id>/materials/", LessonMaterialAPIView.as_view()),
    path("<str:lesson_id>/", LessonAPIView.as_view()),
]