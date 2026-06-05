from django.contrib import admin

from notifications_app.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "recipient", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("title", "message", "recipient__email")
    readonly_fields = ("id", "created_at")
