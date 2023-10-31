from rest_framework import permissions
from manufacturer.models import Employee


class IsUserNetwork(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            try:
                return request.user.employee.is_active or request.auth is not None
            except Employee.DoesNotExist:
                return False
        else:
            return request.auth is not None

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                employee = request.user.employee
                return employee.is_active and employee.id == obj.employee_id
            except Employee.DoesNotExist:
                return False
        else:
            return request.auth is not None

