from rest_framework import serializers

from settings_app.models import AppSetting


class AppSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSetting
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
