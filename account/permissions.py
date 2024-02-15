# users/permissions.py
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        try:
            user, _ = jwt_auth.authenticate(request)
        except Exception as e:
            # Handle authentication errors
            return False

        return user and user.user_role == 'A'


class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        try:
            user, _ = jwt_auth.authenticate(request)
        except Exception as e:
            # Handle authentication errors
            return False

        return user
