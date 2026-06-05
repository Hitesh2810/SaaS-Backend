from rest_framework import serializers

from notifications_app.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("id", "is_read", "created_at")
