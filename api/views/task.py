from rest_framework import viewsets, mixins
from api.serializers.task import TaskSerializer, TaskGetListSerializer
from api.models import Task, Step
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers.step import StepSerializer
from .step_response import StepResponse


class TaskViewSet(viewsets.ModelViewSet):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):

        task_name = self.kwargs.get("taskname", None)

        if task_name:
            tasks = Task.objects.filter(name__icontains=task_name).all()
            return tasks

        return super().get_queryset()
    
    @action(detail=True, methods=["get"], url_name="task-steps")
    def get_steps(self, request, pk=None):
        
        task = Task.objects.filter(id=pk).prefetch_related("steps").first()
        steps_serializer = self.get_serializer(instance=task.steps.all(), many=True)
        
        return StepResponse(steps_serializer.data)
    
    def get_serializer_class(self):

        if self.action == "get_steps":
            self.serializer_class = StepSerializer
        elif self.action == "list" or self.action == "retrieve":
            self.serializer_class = TaskGetListSerializer
        return super().get_serializer_class()
    
