from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "subscription", "amount", "payment_method", "status", "payment_date")
    list_filter = ("status", "payment_method", "payment_date")
    search_fields = ("transaction_id", "subscription__tenant__name")
    readonly_fields = ("id", "created_at")
