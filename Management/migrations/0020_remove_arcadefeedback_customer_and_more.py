# Generated by Django 5.1.4 on 2025-01-24 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0019_staffprofile_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arcadefeedback',
            name='customer',
        ),
        migrations.AddField(
            model_name='arcadefeedback',
            name='customer_contact',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='arcadefeedback',
            name='customer_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='arcadefeedback',
            name='customer_name',
            field=models.CharField(default='admin', max_length=250),
            preserve_default=False,
        ),
    ]
