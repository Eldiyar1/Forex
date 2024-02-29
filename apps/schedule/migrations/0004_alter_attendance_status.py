# Generated by Django 5.0.2 on 2024-02-29 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schedule", "0003_alter_attendance_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="status",
            field=models.PositiveIntegerField(
                choices=[(1, 1), (0, 0)], default=0, verbose_name="Status"
            ),
        ),
    ]
