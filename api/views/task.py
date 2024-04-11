from rest_framework import viewsets, mixins
from api.serializers.task import TaskSerializer
from api.models import Task


class TaskViewSet(viewsets.ModelViewSet):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):

        task_name = self.kwargs.get("taskname", None)

        if task_name:
            tasks = Task.objects.filter(name__icontains=task_name).all()
            return tasks

        return super().get_queryset()