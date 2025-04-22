from django.contrib import admin
from .models import Course, CourseEnrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'teacher', 'min_attendance_percent', 'created_at', 'updated_at')
    list_filter = ('institution', 'teacher', 'created_at')
    search_fields = ('name', 'description', 'institution__name', 'teacher__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'description')
        }),
        ('Details', {
            'fields': ('institution', 'teacher', 'min_attendance_percent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('institution', 'teacher')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('course__name', 'student__username')
    readonly_fields = ('id', 'enrolled_at')
    fieldsets = (
        (None, {
            'fields': ('id', 'course', 'student')
        }),
        ('Timestamps', {
            'fields': ('enrolled_at',)
        }),
    )
    ordering = ('-enrolled_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course', 'student')