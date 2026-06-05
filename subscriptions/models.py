import uuid

from django.db import models


class Subscription(models.Model):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    STATUS_CHOICES = ((ACTIVE, "Active"), (EXPIRED, "Expired"), (CANCELLED, "Cancelled"))
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    BILLING_CHOICES = ((MONTHLY, "Monthly"), (YEARLY, "Yearly"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.CASCADE, related_name="subscriptions")
    plan_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.tenant} - {self.plan_name}"
