from rest_framework import serializers
from api.models.step import Step
from api.models.task import Task
from api.serializers.customlistserializer import CustomListSerializer
 

class StepSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Task.objects.all())
    id = serializers.IntegerField(required=False, read_only=True)


    class Meta:
        model = Step
        fields = ["id",'name','tasks']
        list_serializer_class = CustomListSerializer

    



class StepUpdateSerializer(StepSerializer):
    id = serializers.IntegerField(read_only=False, required=True)
    

    class Meta(StepSerializer.Meta):pass

    def update(self, instance, validated_data):

        id = validated_data.get("id", None)

        if id:
            if Step.objects.filter(id=id).exists():

                return super().update(instance, validated_data)
        return instance
    