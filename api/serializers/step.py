from rest_framework import serializers
from api.models.step import Step
from api.models.task import Task
from api.serializers.customlistserializer import CustomListSerializer
 

class StepSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Task.objects.all())
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Step
        fields = ["id",'name','tasks']
        list_serializer_class = CustomListSerializer