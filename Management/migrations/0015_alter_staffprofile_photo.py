# Generated by Django 5.1.4 on 2025-01-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0014_alter_staffroles_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='staff_photos/'),
        ),
    ]
