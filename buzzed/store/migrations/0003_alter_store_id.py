# Generated by Django 4.2.21 on 2025-06-17 19:38

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
