import copy
from django.test import TestCase
from api.serializers.step import Step
from api.serializers.task import Task
from django.utils import timezone
from django.contrib.auth import get_user_model
from api.serializers.task import TaskSerializer
from api.serializers.step import StepSerializer
import random
import string
User = get_user_model()

class TestStepUpdate(TestCase):
    
    def setUp(self) -> None:
        
        self.user_details = {
            "username": "usr",
            "password": "pswrd"
        }

        user = User(**self.user_details)
        user.save()
        
        self.task_data = {
            "name": "best task ever",
            "description": "best task ever",
            "deadline": timezone.datetime(2030,10,10),
            "priority": Task.Priority.LOW,
            "authors":[user.id],
            "assigned_to":user.id,
            "steps":[{"name":"first step"},{"name":"second step"}]
        }
    
        self.task = TaskSerializer(data=self.task_data)
        
        self.task.is_valid()
        self.task = self.task.save()
        
        self.steps_dict = [{"name":f"Step name Value{index}", "tasks":[]} for index in range(10)]
        
        step_serializer = StepSerializer(data=self.steps_dict, many=True)
        step_serializer.is_valid()
        self.steps = step_serializer.save()
        
        
        return super().setUp()
    
    def test_update_name_to_empty(self):
        
        data = {"name":""}

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=data)
        
        self.assertFalse(step_serializer.is_valid())

    def test_update_name_to_space_symbol(self):
        data = {"name":"   "}

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=data)
        
        self.assertFalse(step_serializer.is_valid())

    def test_update_name_to_digits_only(self):
        data = {"name":"123456"}

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=data)
        
        self.assertTrue(step_serializer.is_valid())

        updated_step = step_serializer.save()

        self.assertEqual(data["name"], updated_step.name)

    def test_update_name_to_none(self):
        data = {"name":None}

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=data)
        
        self.assertFalse(step_serializer.is_valid())
        
    def test_update_name_to_date_value(self):
        data = {"name":timezone.now()}

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=data)
        
        self.assertFalse(step_serializer.is_valid())

    def test_update_name_to_valid_date_value(self):
        data = {"name":f"{timezone.now()}"}

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=data)
        
        self.assertTrue(step_serializer.is_valid())  


    def test_update_name_to_too_long_value(self):
        data = {"name":"".join(random.choices(string.ascii_letters, k=101))}

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=data)
        
        self.assertFalse(step_serializer.is_valid()) 
        
    def test_update_name_to_same_value(self):

        step = self.steps[0]
        step_serializer = StepSerializer(instance=step, data=step.__dict__)
        
        step_serializer.is_valid()
        step = step_serializer.save()

        self.assertEqual(self.steps[0].name,step.name)
        

    def test_update_name_to_same_value_lower(self):
        step = self.steps[0]
        name = step.name
        data = {"name":name.lower()}

        step_serializer = StepSerializer(instance=step, data=data)
        
        step_serializer.is_valid()
        step = step_serializer.save()

        self.assertNotEqual(name,step.name)
        

    def test_update_name_to_same_value_upper(self):
        step = self.steps[0]
        name = step.name
        data = {"name":name.upper()}

        step_serializer = StepSerializer(instance=step, data=data)
        
        step_serializer.is_valid()
        step = step_serializer.save()

        self.assertNotEqual(name,step.name)





