from rest_framework import permissions

class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins can do anything, users can only update their own profile
        return request.user.is_staff or obj == request.user