from rest_framework import permissions
from rest_framework.request import Request


def is_admin(request: Request) -> bool:
    """Check if the request is from an admin user."""
    return request.headers.get("X-ADMIN") == "1"


class CandidatePermission(permissions.BasePermission):
    """Allow anyone to register as a candidate (POST create) or check status."""

    def has_permission(self, request, view):
        return view.action in {"create", "status"}


class AdminOnlyPermission(permissions.BasePermission):
    """Allow only admin (X-ADMIN=1) for admin actions (list, retrieve, update, download, stats, update-status)."""

    admin_actions = {"list", "retrieve", "partial_update", "download_resume"}

    def has_permission(self, request, view):
        if view.action in self.admin_actions:
            return is_admin(request)
        return False
