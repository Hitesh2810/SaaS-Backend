from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import ChangePasswordView, CurrentUserView, LoginView, LogoutView, RegisterView, UserViewSet
from analytics_app.views import DashboardAnalyticsView
from notifications_app.views import NotificationViewSet
from payments.views import PaymentViewSet
from settings_app.views import AppSettingViewSet
from subscriptions.views import SubscriptionViewSet
from tenants.views import TenantViewSet

router = DefaultRouter()
router.register("tenants", TenantViewSet, basename="tenant")
router.register("users", UserViewSet, basename="user")
router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("payments", PaymentViewSet, basename="payment")
router.register("notifications", NotificationViewSet, basename="notification")
router.register("settings", AppSettingViewSet, basename="setting")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", CurrentUserView.as_view(), name="current_user"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("analytics/dashboard/", DashboardAnalyticsView.as_view(), name="dashboard_analytics"),
    path("", include(router.urls)),
]
