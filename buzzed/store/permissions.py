from rest_framework import permissions

class IsManagerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        is_manager = (request.user == obj.manager)
        if request.method == "DELETE":
            if is_manager:
                return True
            else:
                return False
        
        is_admin = request.user in obj.admins.all()
        return is_manager or is_admin