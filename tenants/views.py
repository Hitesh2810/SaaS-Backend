from rest_framework import viewsets

from common.permissions import TenantScopedPermission, is_super_admin
from tenants.models import Tenant
from tenants.serializers import TenantSerializer


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [TenantScopedPermission]
    filterset_fields = ["status", "domain"]
    search_fields = ["name", "domain", "contact_email"]

    def get_queryset(self):
        user = self.request.user
        if is_super_admin(user):
            return Tenant.objects.all()
        if user.tenant_id:
            return Tenant.objects.filter(id=user.tenant_id)
        return Tenant.objects.none()

    def perform_create(self, serializer):
        if not is_super_admin(self.request.user):
            self.permission_denied(self.request, "Only super admins can create tenants.")
        serializer.save()
