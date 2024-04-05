from rest_framework import serializers
from api.models.task import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "authors", "assigned_to", "steps"]
