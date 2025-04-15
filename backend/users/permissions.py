from rest_framework import permissions

from .models import (
    User, Role,
)

from .services import (
    RoleService
)

class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        return user.profile.role == RoleService.get_teacher_role()

