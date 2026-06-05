from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response

from common.permissions import IsSuperOrTenantAdmin, is_super_admin
from payments.models import Payment
from subscriptions.models import Subscription
from tenants.models import Tenant

User = get_user_model()


class DashboardAnalyticsView(APIView):
    permission_classes = [IsSuperOrTenantAdmin]

    def get(self, request):
        tenant_filter = {}
        payment_filter = {"status": Payment.PAID}
        subscription_filter = {"status": Subscription.ACTIVE}
        if not is_super_admin(request.user):
            tenant_filter["tenant_id"] = request.user.tenant_id
            payment_filter["subscription__tenant_id"] = request.user.tenant_id
            subscription_filter["tenant_id"] = request.user.tenant_id

        users = User.objects.filter(**tenant_filter)
        tenants = Tenant.objects.all() if is_super_admin(request.user) else Tenant.objects.filter(id=request.user.tenant_id)
        active_subscriptions = Subscription.objects.filter(**subscription_filter)
        paid_payments = Payment.objects.filter(**payment_filter)

        user_growth = (
            users.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )
        revenue_growth = (
            paid_payments.annotate(month=TruncMonth("payment_date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

        return Response(
            {
                "total_users": users.count(),
                "total_tenants": tenants.count(),
                "active_subscriptions": active_subscriptions.count(),
                "monthly_revenue": paid_payments.aggregate(total=Sum("amount"))["total"] or 0,
                "user_growth": [{"month": row["month"].date().isoformat(), "total": row["total"]} for row in user_growth],
                "revenue_growth": [{"month": row["month"].date().isoformat(), "total": row["total"] or 0} for row in revenue_growth],
            }
        )
