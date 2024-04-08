from dataclasses import dataclass
from rest_framework import serializers
from api.models.task import Task
from api.serializers.step import StepSerializer
from api.serializers.customlistserializer import CustomListSerializer
from django.contrib.auth import get_user_model
from api.models import Step


User = get_user_model()
   

class TaskSerializer(serializers.ModelSerializer):

    steps = StepSerializer(many=True, read_only=False, required=False)
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all().values_list("id", flat=True))
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all().values_list("id", flat=True), required=False)
    name = serializers.CharField(required=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ["id","name", "description", "deadline", "priority", "authors", "assigned_to", "steps"]
        list_serializer_class = CustomListSerializer

    def create(self, validated_data):

        result = {}
        authors = validated_data.pop("authors")
        steps = validated_data.pop("steps")
        assigned_to = validated_data.pop("assigned_to")
        steps_serializer = StepSerializer(data=steps, many=True)

        if steps_serializer.is_valid():
            
            new_task = Task.objects.create(**validated_data)
            steps_model_list = steps_serializer.save()
            new_task.steps.set(steps_model_list)
            new_task.authors.set(authors)
            result = new_task
        else:  
            result["errors"] = steps_serializer.errors

        return result
    
    def update(self, instance, validated_data):

        authors = validated_data.pop("authors", None)
        steps = validated_data.pop("steps", None)

        assigned_to = validated_data.pop("assigned_to", None)


        steps_to_update = Step.objects.filter(tasks__id=instance.id).all()
        steps_serializer = StepSerializer(instance=steps_to_update, data=steps, many=True)

        if steps_serializer.is_valid():
            saved_steps = steps_serializer.save() # will call update because instance is passed
            instance.steps.set(saved_steps["updated"])
        instance.authors.set(authors)

        saved_task = super().update(instance, validated_data)
        saved_task.assigned_to_id = assigned_to
        saved_task.save()

        return saved_task

