from rest_framework import serializers
from api.models.step import Step

class StepSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=False, required=False)

    class Meta:
        model = Step
        fields = ['name','tasks']