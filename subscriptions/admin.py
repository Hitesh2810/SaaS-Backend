from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("tenant", "plan_name", "price", "billing_cycle", "status", "start_date", "end_date")
    list_filter = ("status", "billing_cycle", "start_date")
    search_fields = ("tenant__name", "plan_name")
    readonly_fields = ("id", "created_at", "updated_at")
