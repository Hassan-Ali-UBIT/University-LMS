from rest_framework import permissions

class IsInstitutionAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins of an institution to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user is admin of this institution
        return obj.admin == request.user

class IsInstitutionAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins of an institution to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is admin of this institution
        return obj.admin == request.user
    

    
