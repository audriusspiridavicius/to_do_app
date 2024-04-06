# Generated by Django 5.0.4 on 2024-04-05 19:56

import api.models.task
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(validators=[api.models.task.DeadlineValidator], verbose_name='task deadline'),
        ),
    ]
