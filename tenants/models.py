import uuid

from django.db import models

from common.constants import ACTIVE, TENANT_STATUS_CHOICES


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=TENANT_STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
