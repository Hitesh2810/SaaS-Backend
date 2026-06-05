import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AppSetting",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("category", models.CharField(choices=[("SMTP", "SMTP Settings"), ("APPLICATION", "Application Settings"), ("BRANDING", "Branding Settings"), ("SECURITY", "Security Settings")], max_length=30)),
                ("key", models.CharField(max_length=100)),
                ("value", models.JSONField(default=dict)),
                ("is_secret", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["category", "key"], "unique_together": {("category", "key")}},
        ),
    ]
