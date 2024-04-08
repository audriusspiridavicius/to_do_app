from django.test import TestCase
from api.serializers import StepSerializer, TaskSerializer
from api.models import Task, Step
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
import random
import string
import copy
User = get_user_model()

class TestCreateStep(TestCase):

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
        
        self.steps = [{"name":f"step name value{index}", "tasks":[self.task.id]} for index in range(10)]
        
        
        return super().setUp()

    def test_create_step_no_name(self):

        step_data = {"name":"", "tasks":[self.task.id]}
        step = StepSerializer(data=step_data)

        self.assertFalse(step.is_valid())

    def test_create_step_name_tag_missing(self):

        step_data = {"tasks":[self.task.id]}
        step = StepSerializer(data=step_data)

        self.assertFalse(step.is_valid())

    def test_create_step_valid_name(self):
        step_data = {"name":self.steps[0]["name"], "tasks":[self.task.id]}

        step = StepSerializer(data=step_data)
        step.is_valid()
        step = step.save()

        self.assertTrue(self.steps[0]["name"]==step.name)

    def test_create_step_numbers_name(self):
        step_data = {"name":123456, "tasks":[self.task.id]}

        step = StepSerializer(data=step_data)
        step.is_valid()
        step = step.save()

        self.assertEqual(str(step_data["name"]),step.name)

    def test_create_step_name_space(self):
        step_data = self.steps[0]
        step_data["name"] = " "

        step = StepSerializer(data=step_data)
        self.assertFalse(step.is_valid())
    
    def test_create_step_name_multiple_space(self):
        step_data = self.steps[1]
        step_data["name"] = "          "

        step = StepSerializer(data=step_data)
        self.assertFalse(step.is_valid())
        
    def test_create_step_name_too_long(self):
        step_data = self.steps[5]
        step_data["name"] = "".join(random.choices(population=string.ascii_letters, k=101))
        
        step = StepSerializer(data=step_data)

        self.assertFalse(step.is_valid())
    
    def test_create_step_name_valid_length(self):
        step_data = self.steps[5]
        step_data["name"] = "".join(random.choices(population=string.ascii_letters, k=100))
        
        step = StepSerializer(data=step_data)

        self.assertTrue(step.is_valid())        
        
    def test_create_step_name_special_symbols(self):
        step_data = self.steps[5]
        step_data["name"] = "".join(random.choices(population=string.punctuation+string.printable, k=50))
        step = StepSerializer(data=step_data)

        self.assertTrue(step.is_valid())    
    
    def test_create_step_multiple_same_name(self):
        step_data = self.steps[5]
        
        step1 =  StepSerializer(data=step_data)
        step2 =  StepSerializer(data=step_data)

        step1.is_valid()
        step2.is_valid()

        step1 = step1.save()
        step2 = step2.save()

        self.assertIsNotNone(step1)
        self.assertIsNotNone(step2)

        self.assertNotEqual(step2.id,step1)
        self.assertEqual(step2.name,step1.name)

    def test_create_step_without_task(self):
        step_data = self.steps[0]
        step_data.pop("tasks")

        step =  StepSerializer(data=step_data)
        step.is_valid()
        step = step.save()

        self.assertIsNotNone(step)
        self.assertTrue(Step.objects.filter(id=step.id).exists())

    def test_create_step_non_existing_task(self):
        step_data = self.steps[0]
        step_data["tasks"] = [100]

        step =  StepSerializer(data=step_data)

        self.assertFalse(step.is_valid())


    def test_create_same_step_multiple_task(self):
    
        another_task = copy.deepcopy(self.task_data)

        task_serializer = TaskSerializer(data=another_task)
        task_serializer.is_valid()
        another_task = task_serializer.save()

        step = self.steps[0]
        step["tasks"] = [self.task.id, another_task.id]

        step_serializer = StepSerializer(data=step)
        step_serializer.is_valid()
        step = step_serializer.save()

        self.assertEqual(2, step.tasks.all().count())
        self.assertEqual(5, Step.objects.count())
