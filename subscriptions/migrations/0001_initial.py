import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("tenants", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("plan_name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("billing_cycle", models.CharField(choices=[("MONTHLY", "Monthly"), ("YEARLY", "Yearly")], max_length=20)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("status", models.CharField(choices=[("ACTIVE", "Active"), ("EXPIRED", "Expired"), ("CANCELLED", "Cancelled")], default="ACTIVE", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("tenant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subscriptions", to="tenants.tenant")),
            ],
            options={"ordering": ["-start_date"]},
        ),
    ]
