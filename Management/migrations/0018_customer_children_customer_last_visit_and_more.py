# Generated by Django 5.1.4 on 2025-01-23 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0017_alter_staffroles_role_alter_task_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='children',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='membership',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='membership_id',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.CreateModel(
            name='CustomerVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount_spent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('children', models.SmallIntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='Management.customer')),
            ],
        ),
    ]
