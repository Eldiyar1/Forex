# Generated by Django 5.0.2 on 2024-02-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schedule", "0002_alter_attendance_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="status",
            field=models.PositiveIntegerField(
                choices=[(1, "Present"), (0, "Absent")],
                default=0,
                verbose_name="Status",
            ),
        ),
    ]
