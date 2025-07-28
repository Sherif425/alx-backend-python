from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to ensure users can only access their own messages and conversations.
    Assumes the model has a 'user' field or similar to check ownership.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the owner of the object
        return obj.user == request.user