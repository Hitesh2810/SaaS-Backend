import uuid

from django.db import models


class Payment(models.Model):
    PAID = "PAID"
    PENDING = "PENDING"
    FAILED = "FAILED"
    STATUS_CHOICES = ((PAID, "Paid"), (PENDING, "Pending"), (FAILED, "Failed"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey("subscriptions.Subscription", on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=80)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    payment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date"]

    @property
    def tenant_id(self):
        return self.subscription.tenant_id

    def __str__(self):
        return self.transaction_id
