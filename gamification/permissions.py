from  rest_framework import permissions


class IsStaffOrReadOnly (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff == 1

class IsOwnerOrReadOnly (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj or request.user.is_staff == 1

class IsStaff (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff == 1

class IsOwnerorStaff (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff == 1 or request.user == obj






