# Generated by Django 5.1.4 on 2025-01-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0016_alter_staffprofile_area_of_residence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffroles',
            name='role',
            field=models.CharField(choices=[('Commercial', 'Commercial'), ('Q&A', 'Q&A'), ('Giveaway', 'Giveaway'), ('Ladies Night', 'Ladies Night'), ('Challenges', 'Challenges'), ('Events', 'Events')], max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('Commercial', 'Commercial'), ('Q&A', 'Q&A'), ('Giveaway', 'Giveaway'), ('Ladies Night', 'Ladies Night'), ('Challenges', 'Challenges'), ('Events', 'Events')], max_length=50),
        ),
    ]
