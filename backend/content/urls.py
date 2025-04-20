from django.urls import path

from .views import (
    LessonMaterialAPIView,
    LessonAPIView,
    WatchSessionAPIView,
    WatchSegmentAPIView,
    AttendanceRecordAPIView,
    LessonCommentAPIView,
    CommentReplyAPIView,
)

urlpatterns = [
    path("<str:lesson_id>/comments/", LessonCommentAPIView.as_view()),
    path("<str:lesson_id>/comments/<str:comment_id>/", LessonCommentAPIView.as_view()),
    path("<str:lesson_id>/comments/<str:comment_id>/replies/", CommentReplyAPIView.as_view()),
    path("<str:lesson_id>/attendance/", AttendanceRecordAPIView.as_view()),
    path("<str:lesson_id>/watch-segment/", WatchSegmentAPIView.as_view()),
    path("<str:lesson_id>/watch-session/", WatchSessionAPIView.as_view()),
    path("<str:lesson_id>/materials/", LessonMaterialAPIView.as_view()),
    path("<str:lesson_id>/", LessonAPIView.as_view()),
]