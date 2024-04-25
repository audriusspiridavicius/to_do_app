from dataclasses import dataclass
from rest_framework import serializers
from api.models.task import Task
from api.serializers.step import StepSerializer
from api.serializers.customlistserializer import CustomListSerializer
from django.contrib.auth import get_user_model
from api.models import Step
from api.serializers.user import UserFullNameSerializer

from api.models import UserCustom

   

class TaskSerializer(serializers.ModelSerializer):
    
    steps = StepSerializer(many=True, read_only=False, required=False)
    deadline = serializers.DateTimeField(required=True, format="%Y-%m-%d %H:%M:%S")
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=UserCustom.objects.all(), required=False)
    authors = UserFullNameSerializer(many=True, read_only=False)
    name = serializers.CharField(required=True)

    class Meta:
        model = Task
        fields = ["id","name", "description", "deadline", "priority", "authors", "assigned_to", "steps"]
        list_serializer_class = CustomListSerializer

    def create(self, validated_data):

        authors = validated_data.pop("authors", None) #or None
        
        authors = [author["id"] for author in authors]
        steps = validated_data.pop("steps", None)
        assigned_to = validated_data.pop("assigned_to", None)
        
        new_task = Task.objects.create(**validated_data)
 
        if steps:
            steps_serializer = StepSerializer(data=steps, many=True)

            if steps_serializer.is_valid():
                steps_model_list = steps_serializer.save()
                new_task.steps.set(steps_model_list)
        
        new_task.authors.set(authors)
        new_task.assigned_to = assigned_to
        result = new_task
        return result
    
    def update(self, instance, validated_data):
        authors = validated_data.pop("authors", None)

        authors = [author["id"] for author in authors]
        steps = validated_data.pop("steps", None)
  
        assigned_to = validated_data.pop("assigned_to", None)
        if assigned_to:
            assigned_to = assigned_to.id
        steps_to_update = Step.objects.filter(tasks__id=instance.id).all()
        steps_serializer = StepSerializer(instance=steps_to_update, data=steps, many=True)

        if steps_serializer.is_valid():
            saved_steps = steps_serializer.save() # will call update because instance is passed
            instance.steps.set(saved_steps["updated"])
        instance.authors.set(authors)
        
        saved_task = super().update(instance, validated_data)
        saved_task.assigned_to = UserCustom.objects.filter(id=assigned_to).first()
        saved_task.save()

        return saved_task



