# 🚀 SaaS Dashboard Backend

<div align="center">

![Django](https://img.shields.io/badge/Django-5-green?style=for-the-badge\&logo=django)
![DRF](https://img.shields.io/badge/Django_REST_Framework-red?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue?style=for-the-badge\&logo=postgresql)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge)
![Render](https://img.shields.io/badge/Render-Deployment-purple?style=for-the-badge)

### 🌟 Enterprise Multi-Tenant SaaS Backend

Production-ready Django REST Framework backend powering a complete Multi-Tenant SaaS Platform with Authentication, Tenants, Users, Subscriptions, Payments, Notifications, Analytics, and Settings Management.

</div>

---

# ✨ Features

## 🔐 Authentication & Authorization

### Features

✅ JWT Authentication

✅ Refresh Tokens

✅ Secure Login

✅ Logout Support

✅ Protected APIs

✅ Role-Based Access Control (RBAC)

### Supported Roles

| Role            | Access               |
| --------------- | -------------------- |
| 👑 SUPER_ADMIN  | Full Platform Access |
| 🏢 TENANT_ADMIN | Tenant Level Access  |
| 👤 USER         | Limited User Access  |

---

# 🏢 Tenant Management

Multi-tenant architecture support.

### Features

* Create Tenant
* Update Tenant
* Delete Tenant
* Tenant Status Management
* Tenant Analytics
* Tenant Isolation

---

# 👤 User Management

Complete user lifecycle management.

### Features

* Create User
* Update User
* Delete User
* Search Users
* Filter Users
* Role Assignment
* User Status Management

---

# 📦 Subscription Management

Manage SaaS plans and subscriptions.

### Features

* Create Subscription
* Track Active Plans
* Monitor Expiry
* Billing Cycle Management
* Renewal Tracking

---

# 💳 Payment Management

Centralized payment tracking system.

### Features

* Payment Records
* Revenue Tracking
* Transaction History
* Payment Status Monitoring
* Financial Reporting

---

# 🔔 Notifications

Real-time notification management.

### Features

* Create Notifications
* Send Notifications
* Broadcast Notifications
* Read / Unread Tracking
* User Alerts

---

# 📊 Analytics

Business intelligence and reporting.

### Features

* Revenue Analytics
* User Analytics
* Subscription Analytics
* Tenant Analytics
* Dashboard Statistics

---

# ⚙️ Settings Management

Platform configuration management.

### Features

* General Settings
* Branding Settings
* SMTP Configuration
* Security Settings

---

# 🏗️ Project Structure

```text
backend/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
│
├── tenants/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── subscriptions/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── payments/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── notifications_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── analytics_app/
│   ├── views.py
│   └── urls.py
│
├── settings_app/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py
├── requirements.txt
└── runtime.txt
```

---

# 🔌 API Endpoints

## Authentication

```http
POST /api/auth/login/
POST /api/auth/register/
POST /api/auth/logout/
POST /api/auth/token/refresh/
GET  /api/auth/me/
```

---

## Users

```http
GET    /api/users/
POST   /api/users/
PUT    /api/users/{id}/
DELETE /api/users/{id}/
```

---

## Tenants

```http
GET    /api/tenants/
POST   /api/tenants/
PUT    /api/tenants/{id}/
DELETE /api/tenants/{id}/
```

---

## Subscriptions

```http
GET    /api/subscriptions/
POST   /api/subscriptions/
```

---

## Payments

```http
GET    /api/payments/
POST   /api/payments/
```

---

## Notifications

```http
GET    /api/notifications/
POST   /api/notifications/
```

---

## Analytics

```http
GET /api/analytics/dashboard/
```

---

## Settings

```http
GET  /api/settings/
POST /api/settings/
```

---

# 🗄️ Database

Database Provider:

```text
PostgreSQL (Supabase)
```

### Database Features

✅ Multi-Tenant Support

✅ UUID Primary Keys

✅ Foreign Key Relationships

✅ Secure Data Storage

✅ Cloud Database Hosting

---

# 🔒 Authentication

Authentication Type:

```text
JWT Authentication
```

Features:

* Access Tokens
* Refresh Tokens
* Token Rotation
* Secure Authentication
* Protected Endpoints

Authorization Header:

```http
Authorization: Bearer <access_token>
```

---

# ⚙️ Environment Variables

Create:

```env
backend/.env
```

Add:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=your-host
DB_PORT=5432

ALLOWED_HOSTS=*

CORS_ALLOWED_ORIGINS=http://localhost:3000

SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-key
```

---

# 🚀 Local Development Setup

## Clone Repository

```bash
git clone <repository-url>
```

Move to Backend

```bash
cd backend
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

Create Superuser

```bash
python manage.py createsuperuser
```

Run Development Server

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

Swagger Documentation:

```text
http://127.0.0.1:8000/api/docs/
```

---

# 🌐 Production Deployment

## Render Deployment

### Root Directory

```text
backend
```

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn config.wsgi:application
```

### Environment Variables

Configure all variables from:

```env
backend/.env
```

inside Render Dashboard.

---

# 🔐 Security Features

✅ JWT Authentication

✅ Password Hashing

✅ Role-Based Access Control

✅ Environment Variables

✅ Secure API Access

✅ Token Refresh Support

---

# 🧪 Testing

Run Django Checks

```bash
python manage.py check
```

Apply Migrations

```bash
python manage.py migrate
```

Run Test Suite

```bash
python manage.py test
```

---

# 👨‍💻 Author

## Hitesh Kumar S

🎓 Amrita Vishwa Vidyapeetham

💻 Full Stack Developer

🚀 Django | PostgreSQL | Supabase | REST API Development

---

<div align="center">

### ⭐ Star this repository if you found it useful

Built with ❤️ using Django REST Framework, PostgreSQL, and Supabase.

</div>
