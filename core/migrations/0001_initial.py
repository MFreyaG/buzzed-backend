# Generated by Django 4.2.21 on 2025-07-16 00:23

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("country", models.CharField(max_length=30)),
                ("state", models.CharField(max_length=30)),
                ("city", models.CharField(max_length=30)),
                ("neighborhood", models.CharField(blank=True, max_length=30)),
                ("street", models.CharField(max_length=50)),
                ("number", models.CharField(blank=True, max_length=10)),
                ("complement", models.CharField(blank=True, max_length=30)),
                ("postal_code", models.CharField(blank=True, max_length=15)),
            ],
        ),
    ]
