# Generated by Django 5.1.4 on 2025-01-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0004_remove_task_publishing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='target_type',
            field=models.CharField(choices=[('Marketing', 'Marketing'), ('Management', 'Management')], default='Marketing', max_length=30),
            preserve_default=False,
        ),
    ]
