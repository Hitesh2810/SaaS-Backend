from django.contrib import admin

from settings_app.models import AppSetting


@admin.register(AppSetting)
class AppSettingAdmin(admin.ModelAdmin):
    list_display = ("category", "key", "is_secret", "updated_at")
    list_filter = ("category", "is_secret")
    search_fields = ("category", "key")
    readonly_fields = ("id", "created_at", "updated_at")
