# Generated by Django 5.0.4 on 2024-05-23 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_account_role_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('IsStudent', 'Student'), ('IsLibrarian', 'Librarian'), ('IsAdmin', 'Admin')], default='IsStudent', max_length=100),
        ),
    ]
