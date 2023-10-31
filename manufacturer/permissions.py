from rest_framework import permissions

class IsUserNetwork(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Пользователь аутентифицирован, проверяем, что он активен или аутентифицирован с помощью токена
            return request.user.employee.is_active or request.auth is not None
        else:
            # Пользователь не аутентифицирован, проверяем, что он аутентифицирован с помощью токена
            return request.auth is not None

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # Пользователь аутентифицирован, проверяем, что он имеет доступ к объекту сети или аутентифицирован с помощью токена
            return request.user == obj.employee.user or request.auth is not None
        else:
            # Пользователь не аутентифицирован, проверяем, что он аутентифицирован с помощью токена
            return request.auth is not None

