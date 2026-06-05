import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("subscriptions", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("payment_method", models.CharField(max_length=80)),
                ("transaction_id", models.CharField(max_length=255, unique=True)),
                ("status", models.CharField(choices=[("PAID", "Paid"), ("PENDING", "Pending"), ("FAILED", "Failed")], default="PENDING", max_length=20)),
                ("payment_date", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("subscription", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="payments", to="subscriptions.subscription")),
            ],
            options={"ordering": ["-payment_date"]},
        ),
    ]
