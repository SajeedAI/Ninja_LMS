# Generated by Django 5.1.3 on 2024-11-17 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0003_userassignment_can_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userassignment',
            name='can_view',
        ),
    ]
