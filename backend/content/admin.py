from django.contrib import admin
from .models import (
    Lesson, LessonMaterial, Comment, Reply,
    WatchSession, WatchSegment
)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'video_duration', 'created_at', 'updated_at')
    list_filter = ('course', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    # Make course clickable in admin
    def get_course(self, obj):
        return obj.course.title
    get_course.short_description = 'Course'

    # Optional: Add inline editing for related models
    class LessonMaterialInline(admin.TabularInline):
        model = LessonMaterial
        extra = 1

    class CommentInline(admin.TabularInline):
        model = Comment
        extra = 1

    inlines = [LessonMaterialInline, CommentInline]


@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'lesson', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('file_name', 'file_type')
    date_hierarchy = 'uploaded_at'
    ordering = ('-uploaded_at',)

    def get_lesson(self, obj):
        return obj.lesson.title
    get_lesson.short_description = 'Lesson'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'content_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def get_lesson(self, obj):
        return obj.lesson.title
    get_lesson.short_description = 'Lesson'

    class ReplyInline(admin.TabularInline):
        model = Reply
        extra = 1

    inlines = [ReplyInline]


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'content_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def get_comment(self, obj):
        return obj.comment.content[:50]
    get_comment.short_description = 'Comment'

@admin.register(WatchSession)
class WatchSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'start_time', 'end_time', 'watched_duration', 'last_position', 'created_at')
    list_filter = ('created_at', 'lesson')
    search_fields = ('student__username', 'lesson__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_lesson(self, obj):
        return obj.lesson.title
    get_lesson.short_description = 'Lesson'

    def get_student(self, obj):
        return obj.student.username
    get_student.short_description = 'Student'

    class WatchSegmentInline(admin.TabularInline):
        model = WatchSegment
        extra = 1

    inlines = [WatchSegmentInline]


@admin.register(WatchSegment)
class WatchSegmentAdmin(admin.ModelAdmin):
    list_display = ('watch_session', 'start_position', 'end_position', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('watch_session__id',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_watch_session(self, obj):
        return f"Session {obj.watch_session.id} ({obj.watch_session.student.username})"
    get_watch_session.short_description = 'Watch Session'

