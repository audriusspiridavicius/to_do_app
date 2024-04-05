from django.db import models
from api.models.task import Task

class Step(models.Model):
    name = models.CharField(max_length=100, verbose_name="step title")

    tasks = models.ManyToManyField("Task", through=Task.steps.through)