from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator

User=get_user_model()


class Task(models.Model):
    
    class Priority(models.TextChoices):
        LOW = "low", _("low priority")
        MEDIUM = "medium", _("medium priority")
        HIGH = "high", _("high priority")
        URGENT = "urgent", _("urgent priority")
        CRITICAL = "critical", _("critical priority")
    
    name = models.CharField(max_length=250, verbose_name="task name", blank=False, null=False, validators=[
        MinLengthValidator(10, message="name value has to be at least 10 symbols"),
        MaxLengthValidator(250, message="maximum length is 250 symbols")
        ])
    description = models.TextField(max_length=10000, verbose_name="task description", blank=True, null=True)
    
    deadline = models.DateTimeField(verbose_name="task deadline", blank=False)
    priority = models.CharField(choices=Priority.choices, blank=False, default=Priority.LOW, max_length=10)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    authors = models.ManyToManyField(User, related_name="author_tasks", blank=False)
    assigned_to = models.OneToOneField(User, related_name="tasks", on_delete=models.PROTECT, null=True, blank=True) #Assignee

    steps = models.ManyToManyField("Step")

    def clean(self) -> None:

        self.name = self.name.strip()


        return super().clean()