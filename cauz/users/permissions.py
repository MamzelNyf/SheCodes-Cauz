from rest_framework import permissions

class IsUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(request.method)

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user