import uuid

from django.db import models


class AppSetting(models.Model):
    SMTP = "SMTP"
    APPLICATION = "APPLICATION"
    BRANDING = "BRANDING"
    SECURITY = "SECURITY"
    CATEGORY_CHOICES = (
        (SMTP, "SMTP Settings"),
        (APPLICATION, "Application Settings"),
        (BRANDING, "Branding Settings"),
        (SECURITY, "Security Settings"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    key = models.CharField(max_length=100)
    value = models.JSONField(default=dict)
    is_secret = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("category", "key")
        ordering = ["category", "key"]

    def __str__(self):
        return f"{self.category}:{self.key}"
