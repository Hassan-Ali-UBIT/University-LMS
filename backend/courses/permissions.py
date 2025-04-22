from rest_framework import permissions


class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        return obj.teacher == request.user

class IsCourseStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        return obj.enrollments.filter(student=request.user).exists()

