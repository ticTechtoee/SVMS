# Generated by Django 5.1.5 on 2025-04-08 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
    ]
