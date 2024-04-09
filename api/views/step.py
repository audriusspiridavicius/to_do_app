from rest_framework import viewsets
from api.serializers.step import StepSerializer, StepUpdateSerializer
from api.models.step import Step




class StepViewSet(viewsets.ModelViewSet):

    queryset = Step.objects.all()
    serializer_class = StepSerializer

    def get_serializer_class(self):

        if self.action == "update":
            return StepUpdateSerializer

        return super().get_serializer_class()