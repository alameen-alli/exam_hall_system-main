# Generated by Django 5.0 on 2024-01-18 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invigilator",
            name="hall",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="main.hall",
            ),
        ),
    ]
