from django.db import models
from api.models.task import Task

class Step(models.Model):
    name = models.CharField(max_length=100, verbose_name="step title" , blank=False, null=False)

    tasks = models.ManyToManyField(Task, through=Task.steps.through)

    def __repr__(self) -> str:
        return f"{self.id}-{self.name}({self.tasks.all().count()})"
    
    def __str__(self) -> str:
        return f"{self.name}"