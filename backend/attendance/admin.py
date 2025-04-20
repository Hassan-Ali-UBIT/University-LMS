from django.contrib import admin
from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'watch_percentage', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'lesson')
    search_fields = ('student__username', 'lesson__title')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def get_student(self, obj):
        return obj.student.username
    get_student.short_description = 'Student'

    def get_lesson(self, obj):
        return obj.lesson.title
    get_lesson.short_description = 'Lesson'

