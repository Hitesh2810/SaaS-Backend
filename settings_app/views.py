from rest_framework import viewsets

from common.permissions import IsSuperAdmin
from settings_app.models import AppSetting
from settings_app.serializers import AppSettingSerializer


class AppSettingViewSet(viewsets.ModelViewSet):
    queryset = AppSetting.objects.all()
    serializer_class = AppSettingSerializer
    permission_classes = [IsSuperAdmin]
    filterset_fields = ["category", "key", "is_secret"]
