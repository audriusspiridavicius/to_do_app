# Generated by Django 5.0.4 on 2024-04-05 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_task_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='task description'),
        ),
    ]
