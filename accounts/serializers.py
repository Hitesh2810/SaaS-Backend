from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.constants import SUPER_ADMIN, TENANT_ADMIN, USER
from tenants.models import Tenant

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "tenant", "tenant_name", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("id", "role", "tenant", "tenant_name", "is_active", "created_at", "updated_at")


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name", "role", "tenant", "is_active")
        read_only_fields = ("id",)

    def validate_role(self, value):
        role_map = {"ADMIN": TENANT_ADMIN, "STAFF": USER}
        value = role_map.get(value, value)
        if value not in {SUPER_ADMIN, TENANT_ADMIN, USER}:
            raise serializers.ValidationError("Invalid role.")
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            if value != USER:
                raise serializers.ValidationError("Public registration can only create USER accounts.")
            return value
        if value == SUPER_ADMIN and request.user.role != SUPER_ADMIN:
            raise serializers.ValidationError("Only a super admin can create another super admin.")
        return value

    def validate(self, attrs):
        if not attrs.get("username") and attrs.get("email"):
            base_username = attrs["email"].split("@", 1)[0]
            username = base_username or "user"
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            attrs["username"] = username

        if not attrs.get("password"):
            request = self.context.get("request")
            if request and request.user.is_authenticated:
                attrs["password"] = None
            else:
                raise serializers.ValidationError({"password": "Password is required for registration."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        request = self.context.get("request")
        if (not request or not request.user.is_authenticated) and not validated_data.get("tenant"):
            email = validated_data.get("email", "")
            domain = email.split("@", 1)[1].lower() if "@" in email else f"{validated_data.get('username', 'user')}.local"
            tenant_name = f"{validated_data.get('first_name') or validated_data.get('username') or 'Customer'} Workspace"
            tenant, _ = Tenant.objects.get_or_create(
                domain=domain,
                defaults={"name": tenant_name, "contact_email": email}
            )
            validated_data["tenant"] = tenant
            validated_data["role"] = USER
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        refresh = self.get_token(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token), "user": UserSerializer(user).data}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password", "updated_at"])
        return user


class AssignRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=User._meta.get_field("role").choices)
