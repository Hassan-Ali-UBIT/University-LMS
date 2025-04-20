from rest_framework import permissions

from courses.models import Course


class IsInstitutionAdminOfLesson(permissions.BasePermission):
    """
    Custom permission to only allow admins of an institution to edit it.
    """

    def has_permission(self, request, view):
        lesson_id = view.kwargs.get("lesson_id")
        
        if not request.user.is_authenticated:
            return False

        if not lesson_id:
            return True
        

        course_instance = Course.objects.filter(lessons=lesson_id).first()

        if not course_instance:
            return False
        
        return course_instance.institution.admin == request.user
    