# Multi-Tenant SaaS Admin Backend

Production-ready Django REST backend for a multi-tenant SaaS admin dashboard with JWT auth, RBAC, Supabase PostgreSQL, Swagger docs, filtering, pagination, and a Postman collection.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Update `.env` with your Supabase PostgreSQL credentials:

```env
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db.your-project-ref.supabase.co
DB_PORT=5432
DB_SSLMODE=require
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key
```

## Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`createsuperuser` automatically assigns the SaaS `SUPER_ADMIN` role. Public registration is intentionally limited to `USER`; use `/api/users/` as a super admin or tenant admin to create elevated tenant users.

Swagger documentation is available at:

```text
http://127.0.0.1:8000/api/docs/
```

## Main API Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/`
- `POST /api/auth/change-password/`
- `CRUD /api/tenants/`
- `CRUD /api/users/`
- `POST /api/users/{id}/assign-role/`
- `CRUD /api/subscriptions/`
- `POST /api/subscriptions/{id}/renew/`
- `POST /api/subscriptions/{id}/cancel/`
- `GET /api/subscriptions/history/`
- `CRUD /api/payments/`
- `GET /api/payments/history/`
- `GET /api/analytics/dashboard/`
- `CRUD /api/notifications/`
- `POST /api/notifications/{id}/mark-as-read/`
- `CRUD /api/settings/`

## Sample Requests

Login:

```json
{
  "email": "admin@example.com",
  "password": "StrongPass123!"
}
```

Login response:

```json
{
  "refresh": "eyJ...",
  "access": "eyJ...",
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@example.com",
    "role": "SUPER_ADMIN",
    "tenant": null,
    "is_active": true
  }
}
```

Create tenant:

```json
{
  "name": "Acme Inc",
  "domain": "acme.example.com",
  "contact_email": "ops@acme.example.com",
  "contact_phone": "+15550000000",
  "status": "ACTIVE"
}
```

Dashboard response:

```json
{
  "total_users": 10,
  "total_tenants": 2,
  "active_subscriptions": 2,
  "monthly_revenue": 198.0,
  "user_growth": [{"month": "2026-06-01", "total": 10}],
  "revenue_growth": [{"month": "2026-06-01", "total": 198.0}]
}
```

Import `postman_collection.json` into Postman for a complete endpoint collection.
