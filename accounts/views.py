from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import AssignRoleSerializer, ChangePasswordSerializer, CurrentUserSerializer, LoginSerializer, RegisterSerializer, UserSerializer
from common.constants import SUPER_ADMIN, TENANT_ADMIN
from common.permissions import TenantScopedPermission, is_super_admin, is_tenant_admin

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        RefreshToken(refresh).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."})


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [TenantScopedPermission]
    filterset_fields = ["tenant", "role", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]

    def get_queryset(self):
        user = self.request.user
        if is_super_admin(user):
            return User.objects.select_related("tenant").all()
        if is_tenant_admin(user):
            return User.objects.select_related("tenant").filter(tenant_id=user.tenant_id)
        return User.objects.select_related("tenant").filter(id=user.id)

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        actor = self.request.user
        role = serializer.validated_data.get("role")
        tenant = serializer.validated_data.get("tenant")
        if is_super_admin(actor):
            serializer.save()
            return
        if is_tenant_admin(actor):
            if not tenant:
                tenant = actor.tenant
            if tenant and tenant.id == actor.tenant_id and role != SUPER_ADMIN:
                serializer.save(tenant=tenant)
                return
        self.permission_denied(self.request, "You cannot create users outside your tenant.")

    def perform_update(self, serializer):
        actor = self.request.user
        role = serializer.validated_data.get("role", serializer.instance.role)
        tenant = serializer.validated_data.get("tenant", serializer.instance.tenant)
        if is_super_admin(actor):
            serializer.save()
            return
        if is_tenant_admin(actor) and tenant and tenant.id == actor.tenant_id and role != SUPER_ADMIN:
            serializer.save()
            return
        self.permission_denied(self.request, "You cannot update users outside your tenant or assign SUPER_ADMIN.")

    @action(detail=True, methods=["post"], url_path="assign-role")
    def assign_role(self, request, pk=None):
        target = self.get_object()
        serializer = AssignRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.validated_data["role"]
        if role == SUPER_ADMIN and not is_super_admin(request.user):
            self.permission_denied(request, "Only super admins can assign SUPER_ADMIN.")
        if is_tenant_admin(request.user) and target.tenant_id != request.user.tenant_id:
            self.permission_denied(request, "Cannot assign roles outside your tenant.")
        if is_tenant_admin(request.user) and role == SUPER_ADMIN:
            self.permission_denied(request, "Tenant admins cannot assign SUPER_ADMIN.")
        target.role = role
        target.save(update_fields=["role", "updated_at"])
        return Response(UserSerializer(target).data)
