# Generated by Django 5.1.4 on 2025-01-23 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0018_customer_children_customer_last_visit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='department',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
