from dataclasses import dataclass
from rest_framework import serializers
from api.models.task import Task
from api.serializers.step import StepSerializer
from django.contrib.auth import get_user_model
from api.models import Step
from django.core.exceptions import ValidationError

User = get_user_model()



class TaskListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):

        existing_records = {record.id:record for record in instance}

        created_tasks = []
        updated_tasks = []
        errors = []
        for task in validated_data:
            
            task_id = task.get("id", None)
            task_error = task.get("has_error", None)
            if task_error:
                errors.append(task)
            else:
                if task_id:
                    
                    existing_task_record = existing_records.get(task_id, None)
                    if existing_task_record:
                    
                        tsk = TaskSerializer(existing_task_record,task)
                        if tsk.is_valid():
                            updated_tasks.append(tsk.save())
                        # update existing task
                        else:
                            print(f" tsk not valid = {tsk.errors} - {tsk.error_messages}")
                            errors.append(tsk.errors|existing_task_record.__dict__)
                    else:
                        #create new task
                        tsk = TaskSerializer(data=task)
                        if tsk.is_valid():
                                created_tasks.append(tsk.save())

        return {
            "created":created_tasks,
            "updated":updated_tasks,
            "errors": errors
        }
    def to_representation(self, data):
        
        print()
        print(f"123123213to_representation = {data}")
        print()
        
        
        return super().to_representation(data)
    def to_internal_value(self, data):

        validated_data = []
        errors = []
        
        # self.data = []

        for task in data:
            task_serializer = self.child.__class__(data=task)
            if not  task_serializer.is_valid():
                task["has_error"] = True
                task["error"] = task_serializer.errors
                errors.append({"error":task_serializer.errors|task})
            validated_data.append(task)

        # print()
        # print()
        # print(f"tasks with errors = {errors}")
        # print()
        # print()
        return validated_data
    


class TaskSerializer(serializers.ModelSerializer):

    steps = StepSerializer(many=True, read_only=False, required=False)
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all().values_list("id", flat=True))
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all().values_list("id", flat=True), required=False)
    name = serializers.CharField(required=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ["id","name", "description", "deadline", "priority", "authors", "assigned_to", "steps"]
        list_serializer_class = TaskListSerializer

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
            instance.steps.set(saved_steps)
        instance.authors.set(authors)

        saved_task = super().update(instance, validated_data)
        saved_task.assigned_to_id = assigned_to
        saved_task.save()

        return saved_task

