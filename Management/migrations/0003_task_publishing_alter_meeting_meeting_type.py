# Generated by Django 5.1.4 on 2025-01-14 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0002_remove_task_delegation_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='publishing',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_type',
            field=models.CharField(choices=[('SMM', 'Senior Management Meeting'), ('MM', 'Management Meeting')], max_length=50),
        ),
    ]
