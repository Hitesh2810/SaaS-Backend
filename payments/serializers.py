from rest_framework import serializers

from payments.models import Payment
from subscriptions.models import Subscription
import uuid


class PaymentSerializer(serializers.ModelSerializer):
    tenant = serializers.UUIDField(source="subscription.tenant_id", read_only=True)
    transaction_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("id", "created_at")

    def create(self, validated_data):
        if not validated_data.get("transaction_id"):
            validated_data["transaction_id"] = str(uuid.uuid4())
        return super().create(validated_data)
