from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import TenantScopedPermission, is_super_admin, is_tenant_admin
from notifications_app.models import Notification
from notifications_app.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [TenantScopedPermission]
    filterset_fields = ["recipient", "is_read"]

    def get_permissions(self):
        if self.action == "mark_as_read":
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        qs = Notification.objects.select_related("recipient", "recipient__tenant")
        user = self.request.user
        if is_super_admin(user):
            return qs
        if is_tenant_admin(user):
            return qs.filter(recipient__tenant_id=user.tenant_id)
        return qs.filter(recipient=user)

    def perform_create(self, serializer):
        recipient = serializer.validated_data.get("recipient")
        if not is_super_admin(self.request.user) and recipient.tenant_id != self.request.user.tenant_id:
            self.permission_denied(self.request, "Cannot notify users outside your tenant.")
        serializer.save()

    @action(detail=True, methods=["post"], url_path="mark-as-read")
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(NotificationSerializer(notification).data)
