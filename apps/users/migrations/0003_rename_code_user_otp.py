# Generated by Django 4.2.10 on 2024-03-02 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='code',
            new_name='otp',
        ),
    ]
