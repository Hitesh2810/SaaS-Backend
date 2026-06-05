from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from common.permissions import is_super_admin, is_tenant_admin
from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["subscription", "status", "payment_method"]

    def get_queryset(self):
        qs = Payment.objects.select_related("subscription", "subscription__tenant")
        if is_super_admin(self.request.user):
            return qs
        return qs.filter(subscription__tenant_id=self.request.user.tenant_id)

    def perform_create(self, serializer):
        subscription = serializer.validated_data.get("subscription")
        if not is_super_admin(self.request.user) and subscription.tenant_id != self.request.user.tenant_id:
            self.permission_denied(self.request, "Cannot create payments outside your tenant.")
        serializer.save()

    def perform_update(self, serializer):
        if not (is_super_admin(self.request.user) or is_tenant_admin(self.request.user)):
            self.permission_denied(self.request, "Customers cannot modify payments directly.")
        subscription = serializer.validated_data.get("subscription", serializer.instance.subscription)
        if not is_super_admin(self.request.user) and subscription.tenant_id != self.request.user.tenant_id:
            self.permission_denied(self.request, "Cannot move payments outside your tenant.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (is_super_admin(self.request.user) or is_tenant_admin(self.request.user)):
            self.permission_denied(self.request, "Customers cannot delete payments.")
        return super().perform_destroy(instance)

    @action(detail=False, methods=["get"])
    def history(self, request):
        return self.list(request)
