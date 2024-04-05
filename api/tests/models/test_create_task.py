from django.test import TestCase
from api.models.task import Task
from api.models.step import Step
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
import logging
from dataclasses import dataclass, asdict, field
from django.core.exceptions import ValidationError
import random
import string
import copy



logger = logging.getLogger(__name__)


def get_steps(steps=None):
    
    if not steps:
        steps = ['first step','step1', 'step2', 'step3', 'last step']

    step_list = [Step(name=step).save() for step in steps]

    return step_list


@dataclass(kw_only=True)
class TaskData:

    name: str = "first very easy task"
    description: str = "Lorem ipsum"
    deadline: datetime = make_aware(datetime(2024,10,10,10,0,0))
    priority: Task.Priority = Task.Priority.LOW
    
@dataclass(kw_only=True, frozen=False)
class TaskDataWithRelationships(TaskData):
    authors: list[User] = field(default_factory=list)
    assigned_to: User = User(username="abc", password="123")
    steps: list[Step] = field(default_factory=list)

class TestTaskCreateWithoutRelationships(TestCase):

    def log_data(self):

        logger.warning(f"new_task_on_db.name = {self.new_task_on_db.name} ")
        logger.warning(f"new_task_on_db.description = {self.new_task_on_db.description} ")
        logger.warning(f"new_task_on_db.deadline = {self.new_task_on_db.deadline} ")
        logger.warning(f"new_task_on_db.priority = {self.new_task_on_db.priority} ")
        logger.warning(f"new_task_on_db.authors = {self.new_task_on_db.authors} ")
        logger.warning(f"new_task_on_db.assigned_to = {self.new_task_on_db.assigned_to} ")
        logger.warning(f"new_task_on_db.steps = {self.new_task_on_db.steps} ")
        logger.warning(f"test_data = {self.test_data} ")

    def setUp(self) -> None:

        self.test_data = TaskData()
        self.task = Task(**asdict(TaskData()))

        self.task.save()

        self.new_task_on_db = Task.objects.first()

        return super().setUp()

    
    def test_one_task_record_saved(self):

        records_saved = self.new_task_on_db is not None
        self.assertTrue(records_saved, msg="exactly 1 task should be created")

    def test_task_created(self):

        tasks_exists = Task.objects.exists()
        self.assertEqual(True,tasks_exists)
    
    def test_task_name(self):

        created_task = Task.objects.filter(id=self.task.id).first()
        self.assertEqual(self.test_data.name,created_task.name, msg=f"task name should be -> {self.test_data.name}")
    
    def test_task_authors_None(self):

        self.assertEqual(0,len(self.new_task_on_db.authors.all()), msg="should be no authors because not assigned")
    
    def test_task_assigned_to_None(self):

        self.assertTrue(self.new_task_on_db.assigned_to is None, msg=" authors should be null because not assigned")
    
    def test_task_has_no_steps(self):

        self.assertTrue(len(self.new_task_on_db.steps.all())==0)

    def test_task_has_correct_priority(self):

        self.log_data()
        self.assertTrue(Task.Priority.LOW==self.new_task_on_db.priority)

class TestTaskCreateWithRelationships(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_data = TaskDataWithRelationships()

        return super().setUpTestData()
    
    def setUp(self) -> None:
        self.username = "test user"
        self.password = "12345"

        self.user = User(username=self.username, password=self.password)
        self.user.save()

        self.test_data.authors.append(self.user)
        self.test_data.assigned_to = self.user
        self.test_data.steps = []

        self.step1 = Step(name="pirmas zingsnis")
        self.step2 = Step(name="antras zingsnis")
        
        self.step1.save()
        self.step2.save()

        self.task = Task(name=self.test_data.name, description=self.test_data.description, deadline=self.test_data.deadline, priority=self.test_data.priority)
        self.task.save()
        
        self.task.authors.set(self.test_data.authors)
        self.task.assigned_to = self.test_data.assigned_to
        self.task.steps.set([self.step1,self.step2])
        self.task.save()

        return super().setUp()

    def test_create_task_valid_all_data(self):
        
        new_task_created = Task.objects.all().count()
        self.assertEqual(1,new_task_created)
    
    def test_author_usrname_password(self):

        author = User.objects.first()

        self.assertTrue(author, msg="new user should be saved")
        self.assertEqual(author.username, self.username, msg="username should match")
        self.assertEqual(author.password, self.password, msg="password value should match")

    def test_task_has_author(self):

        task = Task.objects.filter(id=self.task.id).prefetch_related("authors").first()

        authors = task.authors.all()

        authors_count = len(authors)

        self.assertEqual(1,authors_count)
        self.assertEqual(self.user.username, authors.first().username)
    
    def test_task_has_assigned_to(self):

        task = Task.objects.filter(id=self.task.id).first()

        assigned_to = task.assigned_to
        
        self.assertIsNotNone(task)
        self.assertIsNotNone(assigned_to, msg="task should have assignee")
        self.assertEqual(1,assigned_to.id)
        self.assertEqual(self.username, assigned_to.username)

    def test_task_has_steps(self):

        task = Task.objects.filter(id=self.task.id).prefetch_related("steps").first()

        steps = task.steps.all()

        steps_count = len(steps)

        self.assertEqual(2, steps_count)
        self.assertEqual(self.step1.name, steps[0].name)
        self.assertEqual(self.step2.name, steps[1].name)


class TestTaskName(TestCase):

    def setUp(self) -> None:

        self.username = "username"
        self.password = "password"

        self.author = User(username=self.username, password=self.password)

        self.author.save()


        self.task = Task(**asdict(TaskData()))
        self.task.save()
        self.task.authors.set([self.author])
        self.task.steps.set(get_steps())


        return super().setUp()
    
    def test_task_name_not_set(self):

        self.task.name = ""
        
        with self.assertRaisesMessage(ValidationError, expected_message="This field cannot be blank."):
            self.task.full_clean()
   
    def test_task_name_too_short(self):

        self.task.name = "a12345"
        
        with self.assertRaisesMessage(ValidationError, expected_message="name value has to be at least 10 symbols"):
            self.task.full_clean()

    def test_task_name_too_long(self):

        random_string = random.choices(string.ascii_lowercase,k=251)
        random_string = "".join(random_string)

        self.task.name = random_string
        
        with self.assertRaisesMessage(ValidationError, expected_message="maximum length is 250 symbols"):
            self.task.full_clean()

    def test_task_name_traling_leading_space(self):

        original_name = self.task.name

        self.task.name = f"   {original_name}    "

        self.task.full_clean()
        self.task.save()

        saved_name = Task.objects.first().name

        self.assertEqual(original_name, saved_name, msg="leading space should be removed")


    def test_task_create_2_tasks_same_name(self):

        second_task = copy.deepcopy(self.task)

        second_task.id = None
        second_task.full_clean()

        self.task.full_clean()
        self.task.save()
        second_task.save()


        self.assertNotEqual(self.task.id, second_task.id)

        task_count = Task.objects.count()

        self.assertEqual(2, task_count, msg="should be able to create task with same name value")
        self.assertEqual(Task.objects.all()[0].name,Task.objects.all()[1].name, msg="Task names should match")












