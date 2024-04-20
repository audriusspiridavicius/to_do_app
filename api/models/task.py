from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

User=get_user_model()



def DeadlineValidator(deadline:timezone.datetime) -> Any:

    valid_year = deadline.year >= timezone.now().year
    valid_month = deadline.month >= timezone.now().month
    
    if not valid_year:
        raise ValidationError(message=f"year value({deadline.year}) is not valid!")
    elif deadline.year == timezone.now().year and not valid_month:
        raise ValidationError(message=f"month value({deadline.month}) is not valid!")
    elif deadline.year == timezone.now().year and deadline.month == timezone.now().month and deadline.day < timezone.now().day:
        raise ValidationError(message=f"day value({deadline.day}) is not valid!")




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

        ], error_messages={"required": "Name field is required!"})
    description = models.TextField(max_length=10000, verbose_name="task description", blank=True, null=True)
    
    deadline = models.DateTimeField(verbose_name="task deadline", blank=False, validators=[DeadlineValidator])
    priority = models.CharField(choices=Priority.choices, blank=True, default=Priority.LOW, max_length=10)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    authors = models.ManyToManyField(User, related_name="author_tasks", blank=False)
    assigned_to = models.ForeignKey(User, related_name="tasks", on_delete=models.PROTECT, null=True, blank=True) #Assignee

    steps = models.ManyToManyField("Step")

    def clean(self) -> None:

        self.name = self.name.strip()


        return super().clean()
    
    def __str__(self) -> str:
        return f"{self.name}"