from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "username", "role", "tenant", "is_active", "created_at")
    list_filter = ("role", "tenant", "is_active", "is_staff")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at", "last_login", "date_joined")
    fieldsets = DjangoUserAdmin.fieldsets + (("SaaS", {"fields": ("role", "tenant", "created_at", "updated_at")}),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (("SaaS", {"fields": ("email", "role", "tenant")}),)
