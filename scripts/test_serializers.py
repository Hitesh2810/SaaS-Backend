import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import pathlib
BASE = pathlib.Path(__file__).resolve().parents[1]
import sys
sys.path.append(str(BASE))

django.setup()

from tenants.serializers import TenantSerializer
from payments.serializers import PaymentSerializer
from subscriptions.models import Subscription
from tenants.models import Tenant

print('--- TenantSerializer test ---')
tenant_payload = {'name':'ACME','domain':'acme.local','contact_email':'admin@acme.local'}
ser = TenantSerializer(data=tenant_payload)
print('valid', ser.is_valid())
print('errors', ser.errors)
print('validated_data', getattr(ser,'validated_data', None))

print('\n--- PaymentSerializer setup ---')
sub = Subscription.objects.first()
if not sub:
    print('No subscription found; creating test tenant and subscription')
    t = Tenant.objects.create(name='Tmp', domain='tmp.local', contact_email='tmp@example.com')
    sub = Subscription.objects.create(tenant=t, plan_name='Test Plan', price='10.00', billing_cycle='MONTHLY', start_date=date.today(), end_date=date.today())
else:
    print('Found existing subscription', sub.id)

payment_payload = {'subscription': str(sub.id), 'amount': '12.34', 'transaction_id': 'tx-test-123', 'status': 'PAID', 'payment_method': 'CARD', 'payment_date': '2026-06-03T00:00:00Z'}
ps = PaymentSerializer(data=payment_payload)
print('payment valid', ps.is_valid())
print('payment errors', ps.errors)
print('payment validated_data', getattr(ps,'validated_data', None))
