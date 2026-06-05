import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from common.constants import ROLE_CHOICES, SUPER_ADMIN, USER


class SaaSUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", SUPER_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return super().create_superuser(username, email=email, password=password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    tenant = models.ForeignKey("tenants.Tenant", on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SaaSUserManager()

    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email or self.username
