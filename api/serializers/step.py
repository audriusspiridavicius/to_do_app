from rest_framework import serializers
from api.models.step import Step
from api.models.task import Task


class StepListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):

        instance_dict = {step.id: step for step in instance}
        
        result_list = []
        for step in validated_data:
            #if step has id than update else create
            step_id = step.get("id", None)
            if not step_id:
                created_step = Step.objects.create(**step)
                result_list.append(created_step)
            else:
                existing_step = instance_dict.get(step_id, None)
                if existing_step:
                    
                    existing_step = Step.objects.filter(id=existing_step.id).first()
                    existing_step.name = step["name"]
                    existing_step.save()
                    # updated_step = StepSerializer.update(instance=existing_step,data=step)
                    result_list.append(existing_step)
            
        return result_list
    

class StepSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Task.objects.all())
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Step
        fields = ["id",'name','tasks']
        list_serializer_class = StepListSerializer