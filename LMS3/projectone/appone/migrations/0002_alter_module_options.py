# Generated by Django 5.1.3 on 2024-11-17 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appone', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'permissions': [('can_view_module', 'Can view module')]},
        ),
    ]
