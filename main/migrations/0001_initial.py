# Generated by Django 5.0 on 2024-01-18 10:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=8)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.department",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="department",
            name="faculty",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.faculty"
            ),
        ),
        migrations.CreateModel(
            name="Hall",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("capacity", models.PositiveIntegerField()),
                ("description", models.CharField(max_length=256)),
                ("num_columns", models.PositiveIntegerField(default=0)),
                ("num_rows", models.PositiveIntegerField(default=0)),
                ("courses", models.ManyToManyField(to="main.course")),
                (
                    "invigilators",
                    models.ManyToManyField(
                        blank=True, related_name="halls", to="accounts.invigilator"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.course"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offer",
                        to="accounts.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Seat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position_x", models.IntegerField()),
                ("position_y", models.IntegerField()),
                (
                    "hall",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.hall"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TimeTable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exam_date", models.DateField()),
                ("exam_time", models.TimeField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.course"
                    ),
                ),
            ],
        ),
    ]