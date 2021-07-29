from rest_framework.permissions import BasePermission
from nora.choices import employee, nora


class EmployeePermission(BasePermission):
    """
    Class for evaluate user rol It needs to be logged in and that
    the user role is that of an employee
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.profile.role == employee)


class NoraPermission(BasePermission):
    """
    Class for evaluate user rol It needs to be logged in and that
    the user role is that of an nora
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.profile.role == nora)