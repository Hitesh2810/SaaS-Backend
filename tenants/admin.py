from django.contrib import admin

from tenants.models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "domain", "contact_email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "domain", "contact_email")
    readonly_fields = ("id", "created_at", "updated_at")
