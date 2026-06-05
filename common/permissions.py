from rest_framework.permissions import BasePermission, SAFE_METHODS

from common.constants import SUPER_ADMIN, TENANT_ADMIN, USER


def is_super_admin(user):
    return bool(user and user.is_authenticated and user.role == SUPER_ADMIN)


def is_tenant_admin(user):
    return bool(user and user.is_authenticated and user.role == TENANT_ADMIN)


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_super_admin(request.user)


class IsSuperOrTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_super_admin(request.user) or is_tenant_admin(request.user)


class TenantScopedPermission(BasePermission):
    """
    SUPER_ADMIN can do everything. TENANT_ADMIN can manage records in their tenant.
    USER is restricted to safe access to their own user-scoped resources.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if is_super_admin(request.user):
            return True
        if is_tenant_admin(request.user):
            return True
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        user = request.user
        if is_super_admin(user):
            return True

        obj_tenant_id = getattr(obj, "tenant_id", None)
        if obj_tenant_id and is_tenant_admin(user):
            return obj_tenant_id == user.tenant_id

        recipient_id = getattr(obj, "recipient_id", None)
        if recipient_id:
            return recipient_id == user.id

        if obj.__class__.__name__ == "User":
            if user.role == USER:
                return request.method in SAFE_METHODS and obj.id == user.id
            return is_tenant_admin(user) and obj.tenant_id == user.tenant_id

        return False
