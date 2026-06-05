from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import is_super_admin, is_tenant_admin
from subscriptions.models import Subscription
from subscriptions.serializers import RenewSubscriptionSerializer, SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["tenant", "status", "billing_cycle", "plan_name"]

    def get_queryset(self):
        qs = Subscription.objects.select_related("tenant")
        if is_super_admin(self.request.user):
            return qs
        return qs.filter(tenant_id=self.request.user.tenant_id)

    def perform_create(self, serializer):
        tenant = serializer.validated_data.get("tenant")
        if not is_super_admin(self.request.user) and tenant.id != self.request.user.tenant_id:
            self.permission_denied(self.request, "Cannot create subscriptions outside your tenant.")
        serializer.save()

    def perform_update(self, serializer):
        if not (is_super_admin(self.request.user) or is_tenant_admin(self.request.user)):
            self.permission_denied(self.request, "Customers cannot modify subscriptions directly.")
        tenant = serializer.validated_data.get("tenant", serializer.instance.tenant)
        if not is_super_admin(self.request.user) and tenant.id != self.request.user.tenant_id:
            self.permission_denied(self.request, "Cannot move subscriptions outside your tenant.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (is_super_admin(self.request.user) or is_tenant_admin(self.request.user)):
            self.permission_denied(self.request, "Customers cannot delete subscriptions.")
        return super().perform_destroy(instance)

    @action(detail=True, methods=["post"])
    def renew(self, request, pk=None):
        subscription = self.get_object()
        serializer = RenewSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription.end_date = serializer.validated_data["end_date"]
        subscription.status = Subscription.ACTIVE
        if "price" in serializer.validated_data:
            subscription.price = serializer.validated_data["price"]
        subscription.save()
        return Response(SubscriptionSerializer(subscription).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        subscription = self.get_object()
        subscription.status = Subscription.CANCELLED
        subscription.save(update_fields=["status", "updated_at"])
        return Response(SubscriptionSerializer(subscription).data)

    @action(detail=False, methods=["get"])
    def history(self, request):
        return self.list(request)
