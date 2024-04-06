from django.test import TestCase
from api.models.step import Step
from api.models.task import Task
from django.core.exceptions import ValidationError
import string
import random
from django.utils import timezone

class TestStep(TestCase):

    def __create_task(self,data):
        
        task = Task(**data)
        task.full_clean()
        task.save()

        return task
    
    def setUp(self) -> None:

        self.task_data = {
            "name": "task number 1",
            "description": "task description",
            "deadline": timezone.now(),
            "priority": Task.Priority.MEDIUM
        }
        

        self.task = self.__create_task(self.task_data)
        self.task2 = self.__create_task(self.task_data)

        
        self.name_valid = "first step of task"
        self.name_empty = ""
        self.name_too_long = "".join(random.choices(string.ascii_letters, k=101))

        self.step = Step()
        self.step.save()
        


        return super().setUp()
    
    def test_step_name_valid(self):

        self.step.name = self.name_valid
        
        step_is_valid = False
        try:
            with self.assertRaises(ValidationError):
                self.step.full_clean()
                self.step.save()

        except AssertionError:
            step_is_valid = True
            
        self.assertTrue(step_is_valid, msg=f"step ({self.step.__dict__}) should be valid!!!")
        tasks = self.step.tasks.all()
        self.assertTrue(len(tasks)==0, msg="Step is not assigned to any task. so should be no task records")

    def test_step_name_empty(self):

        self.step.name = self.name_empty

        with self.assertRaises(ValidationError):
            self.step.full_clean()

    def test_step_name_too_long(self):

        self.step.name = self.name_too_long

        with self.assertRaises(ValidationError):
            self.step.full_clean()

    def test_step_assign_task(self):

        self.step.tasks.set([self.task])

        self.assertTrue(self.step.tasks.all().count()==1)

    def test_step_assign_multiple_tasks(self):

        self.step.tasks.set([self.task,self.task2])

        self.assertTrue(self.step.tasks.all().count()==2)