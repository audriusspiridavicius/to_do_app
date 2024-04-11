from rest_framework import viewsets, mixins
from api.serializers.step import StepSerializer, StepUpdateSerializer
from api.serializers.task import TaskSerializer
from api.models.step import Step, Task
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, F, Value


class StepViewSet(viewsets.ModelViewSet):

    queryset = Step.objects.all()
    serializer_class = StepSerializer
    
    def get_serializer_class(self):

        
        if self.action == "update":
            return StepUpdateSerializer
        elif self.action == "get_tasks":
            return TaskSerializer
        return super().get_serializer_class()
    
    
    @action(detail=False,methods=["get","post"], name="step belongs to thease tasks", url_name="step_tasks")
    def steps_odd_id_list(self, request):
        """sample custom viewset action"""

        self.serializer_class = StepSerializer
        serializer = self.get_serializer(instance=Step.objects.annotate(is_odd=F("id")%2).exclude(is_odd=0), many=True)
        
        return Response(serializer.data)
    

    # create custom action that returns list of tasks which have that specific step
    @action(detail=True, methods=["get"], name="get tasks",  url_name="tasks")
    def get_tasks(self, request, pk=None):
        
        tasks = self.get_serializer(instance=Task.objects.filter(steps__id=pk).all(), many=True)

        return Response(tasks.data)