# Generated by Django 5.1.4 on 2025-01-05 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='event',
            new_name='code',
        ),
    ]
