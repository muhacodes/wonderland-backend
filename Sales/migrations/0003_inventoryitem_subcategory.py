# Generated by Django 5.1.4 on 2025-01-21 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0002_category_rename_event_sale_event_sale_event_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='subcategory',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Sales.subcategory'),
            preserve_default=False,
        ),
    ]
