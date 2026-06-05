SUPER_ADMIN = "SUPER_ADMIN"
TENANT_ADMIN = "TENANT_ADMIN"
USER = "USER"

ROLE_CHOICES = (
    (SUPER_ADMIN, "Super Admin"),
    (TENANT_ADMIN, "Tenant Admin"),
    (USER, "User"),
)

ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
SUSPENDED = "SUSPENDED"
TRIAL = "TRIAL"

TENANT_STATUS_CHOICES = (
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (SUSPENDED, "Suspended"),
    (TRIAL, "Trial"),
)
