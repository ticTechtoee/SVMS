# Generated by Django 5.1.5 on 2025-03-07 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.CharField(default='Riyadh', max_length=100),
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.CharField(default='KSA', max_length=100),
        ),
    ]
