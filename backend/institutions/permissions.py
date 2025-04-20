from rest_framework import permissions
from courses.models import Course
from .models import InstitutionMember, Institution

class IsInstitutionAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins of an institution to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is admin of this institution
        return obj.admin == request.user

class IsInstitutionAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins of an institution to edit it.
    """
    def has_permission(self, request, view):
        institution_id = view.kwargs.get("institution_id")

        if not request.user.is_authenticated:
            return False
        
        if not institution_id and request.method in permissions.SAFE_METHODS:
            return True  # or True if you want to allow access in non-institution views
        
        institution_instance = Institution.objects.filter(id=institution_id).first()

        if not institution_instance and  request.method in permissions.SAFE_METHODS:
            return True
        

        return institution_instance.admin == request.user

    def has_object_permission(self, request, view, obj):
        # Check if user is admin of this institution
        if isinstance(obj, Institution):
            return obj.admin == request.user
        elif isinstance(obj, Course):
            return obj.institution.admin == request.user
        else:
            raise NotImplementedError


class IsInstitutionAdminOfCourse(permissions.BasePermission):
    """
    Custom permission to only allow admins of an institution to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user is admin of this institution
        if not request.user.is_authenticated:
            return False
        
        return obj.institution.admin == request.user
        

class IsInstitutionMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Check if user is admin of this institution
        if not request.user.is_authenticated:
            return False
        
        return InstitutionMember.objects.filter(institution=obj, user=request.user).exists()
    
