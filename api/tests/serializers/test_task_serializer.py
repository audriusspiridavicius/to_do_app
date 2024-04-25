from django.test import TestCase
from api.models import Task, Step
from django.utils import lorem_ipsum
from django.utils import timezone
from django.contrib.auth import get_user_model
from api.serializers import TaskSerializer
from api.tests.base_test_class import BaseTestClass
from api.tests.set_up_database import TestSetUptestDatabase
from django.core.exceptions import ValidationError
from api.models import UserCustom as User
import copy




def create_test_data_on_database():

    users = [{"email":f"testemail{index}@email.com","password":f"pswrd{index}"} for index in range(10)]
    userlist = [ User(**user_details) for user_details in users]
    
    # create users
    db_users = User.objects.bulk_create(userlist)

    task_1_steps = [Step(**{"name":"first task first step"}),Step(**{"name":"first task second step"})]
    task_2_steps = [Step(**{"name":"second task first step"}),Step(**{"name":"second task second step"})]

    
    task_1_steps = Step.objects.bulk_create(task_1_steps)
    task_2_steps = Step.objects.bulk_create(task_2_steps)
    
    
    task_1 = {
            "name": "first task ",
            "description": "first task description",
            "deadline": timezone.datetime(2030,10,10),
            "priority": Task.Priority.LOW,
            "assigned_to":db_users[0],  
        }
    
    task_2 = copy.deepcopy(task_1)
    task_2["name"] = "second task"
    task_2["description"] = "desc second task desc"
    task_2["priority"] = Task.Priority.HIGH


    task1 = Task.objects.create(**task_1)
    task2 = Task.objects.create(**task_2)

    task1.steps.set(task_1_steps)
    task2.steps.set(task_2_steps)



class TestTaskSerializerCreateMethod(TestCase, BaseTestClass):
    serializer_class = TaskSerializer
    model_class = Task
    

    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.user_details = {
            "email": "test@email.com",
            "password": "pswrd"
        }
        
        user = User(**cls.user_details)
        user.save()
        
        cls.task_test_data = {
            "name": "Create registration functionality",
            "description": lorem_ipsum.sentence(),
            "deadline": timezone.make_aware(timezone.datetime(2030,10,12)),
            "priority": Task.Priority.LOW,
            "authors":[{"id":user.id, "fullname":user.get_full_name()}],
            "assigned_to":user.id,
            "steps":[{"name":"first step"},{"name":"second step"}]
        }

        return super().setUpTestData()
    

    def test_task_created(self):
        

        self.save_serializer(data=self.task_test_data)

        self.assertTrue(len(Task.objects.all())==1)

    def test_create_task_no_steps(self):

        self.task_test_data.pop("steps")
        
        new_task = self.save_serializer(data=self.task_test_data)

        self.assertIsNotNone(new_task)
        self.assertEqual(1,len(Task.objects.all()))
    
    def test_create_task_no_description(self):
        self.task_test_data.pop("description")
        
        new_task = self.save_serializer(data=self.task_test_data)

        self.assertIsNotNone(new_task)
        self.assertEqual(1,len(Task.objects.all()))
    
    def test_create_task_no_deadline(self):
        self.task_test_data.pop("deadline")
        
        with self.assertRaises(ValidationError):
            self.save_serializer(data=self.task_test_data)

    def test_create_task_no_priority(self):
        self.task_test_data.pop("priority")
        
        task = self.save_serializer(data=self.task_test_data)

        self.assertEqual(1,Task.objects.count())

    def test_create_task_no_authors(self):
        self.task_test_data.pop("authors")
        
        with self.assertRaises(ValidationError):
            self.save_serializer(data=self.task_test_data)
    
    def test_create_task_no_assigned_to(self):
        self.task_test_data.pop("assigned_to")
        
        task = self.save_serializer(data=self.task_test_data)

        self.assertIsNotNone(task)
        self.assertEqual(1,Task.objects.count())


    def test_task_name_saved(self):

        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(self.task_test_data["name"],saved_task.name)

    def test_task_description_saved(self):
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(self.task_test_data["description"],saved_task.description)

    def test_task_deadline_saved(self):
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(self.task_test_data["deadline"],saved_task.deadline)

    def test_task_priority_saved(self):
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(self.task_test_data["priority"],saved_task.priority)
    
    def test_task_created_saved(self):
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(saved_task.created.strftime("%Y-%m-%d"),timezone.now().strftime("%Y-%m-%d"))

    def test_task_modified_saved(self):
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(saved_task.modified.strftime("%Y-%m-%d"),timezone.now().strftime("%Y-%m-%d"))
    
    def test_task_authors_saved(self):
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(self.task_test_data["authors"],list(saved_task.authors.values_list("id", flat=True).all())) 

    def test_task_assigned_to_saved(self):
       
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(self.task_test_data["assigned_to"], saved_task.assigned_to.id) 

    def test_task_steps_saved(self):
        saved_task = self.save_serializer(data=self.task_test_data)
        self.assertEqual(self.task_test_data["steps"], list(saved_task.steps.values("name").all()))     


class TestTaskUpdate(TestCase):


    @classmethod
    def setUpTestData(cls) -> None:
        create_test_data_on_database()
        
        user = User.objects.filter(id=1).first()
        cls.task_test_data = {
            "name": "Create registration functionality",
            "description": lorem_ipsum.sentence(),
            "deadline": timezone.datetime(2030,10,12),
            "priority": Task.Priority.LOW,
            "authors":[{"id":user.id, "fullname":user.get_full_name()}],
            "assigned_to":1,
            "steps":[{"name":"first step"},{"name":"second step"}]
        }

        cls.task_update_data = copy.deepcopy(cls.task_test_data)


    
        task_serializer = TaskSerializer(data=cls.task_test_data)
        task_serializer.is_valid()
        
        cls.task = task_serializer.save()

        cls.task_update_data["id"] = cls.task.id
        cls.task_update_data["description"] = "updated description"
        cls.task_update_data["steps"] = [{"id": cls.task.steps.all()[0].id, "name":"first step 2"},{"id": cls.task.steps.all()[1].id,"name":"second step 2"}]

        return super().setUpTestData()
    

    def test_task_single_update(self):

        task_to_update = Task.objects.filter(id=self.task.id).first()
        task_update_serializer = TaskSerializer(task_to_update,self.task_update_data)

        task_update_serializer.is_valid()
        updated_task = task_update_serializer.save()

        self.assertEqual(self.task_update_data["description"],updated_task.description)
    

class TestMultipleTaskUpdate(TestCase):
    
    def __save_serializer(self,**kwargs):

        serializer = TaskSerializer(**kwargs)
        serializer.is_valid()
        return serializer.save()
    
    
    @classmethod
    def setUpTestData(cls) -> None:
        create_test_data_on_database()

        usr = User.objects.filter(id=1).first()
        authors = [{"id":usr.id,"fullname":usr.get_full_name()}]
        
        cls.task_test_data = {
            "name": "test registration functionality. some random name",
            "description": lorem_ipsum.sentence(),
            "deadline": timezone.datetime(2030,10,20),
            "priority": Task.Priority.LOW,
            "authors":authors,
            "assigned_to":1,
            "steps":[{"name":"first step"},{"name":"second step"}]
        }
        cls.tasks_to_update = Task.objects.filter(id__in=[1,2]).all()

        cls.id1 = 1
        cls.id2 = 2
        
        
        cls.task = copy.deepcopy(cls.task_test_data)
        cls.task["id"] = cls.id1
        cls.task2 = copy.deepcopy(cls.task)
        cls.task2["id"] = cls.id2

        cls.task["id"] = cls.tasks_to_update[0].id
        cls.task["description"] = "updated description"
        cls.task["steps"] = [{"id": cls.tasks_to_update[0].steps.all()[0].id, "name":"first step 2"},{"id": cls.tasks_to_update[0].steps.all()[1].id,"name":"second step 2"}]

        return super().setUpTestData()
    
    def test_task_multiple_update(self):

        task_update_serializer = TaskSerializer(self.tasks_to_update[0],self.task)

        task_update_serializer.is_valid()
        updated_tasks = task_update_serializer.save()

        updated_steps = Task.objects.filter(id=updated_tasks.id).first()
        updated_steps = updated_steps.steps.all()

        self.assertEqual(updated_steps[0].name, self.task["steps"][0]["name"])
        self.assertEqual(updated_steps[1].name, self.task["steps"][1]["name"])


    def test_task_update_multiple_records(self):

        new_user = User(email="test@email.com", password="jonas")
        new_user.save()
        
        self.task_test_data["id"] = self.id1
        task_test_data = [self.task_test_data, self.task_test_data, self.task_test_data]
        task_test_data[2]["assigned_to"] = new_user.id

        task_serializer = TaskSerializer(instance=[self.tasks_to_update[0]], data=task_test_data, many=True)

        task_serializer.is_valid()
        updated_tasks = task_serializer.save()

        self.assertEqual(3,len(updated_tasks["updated"]), msg="updaating same record 3 times")

    def test_task_update_multiple_task_same_name(self):
         
        self.task2["name"] = self.task["name"]

        updated_tasks = self.__save_serializer(instance=self.tasks_to_update,data=[self.task,self.task2], many=True)
        updated_tasks = updated_tasks["updated"]

        self.assertEqual(2,len(updated_tasks))
        self.assertEqual(self.task["name"],updated_tasks[0].name)
        self.assertEqual(self.task["name"],updated_tasks[1].name)
    
    def test_update_multiple_tasks_no_steps(self):
        
        self.task.pop("steps")
        self.task2.pop("steps")

        result = self.__save_serializer(instance=self.tasks_to_update, data=[self.task2,self.task], many=True)

        self.assertEqual(2,len(result["updated"]))
        self.assertEqual(self.task["name"],result["updated"][0].name)
        self.assertEqual(self.task["name"],result["updated"][1].name)

        
    def test_update_multiple_tasks_no_description(self):
        
        self.task.pop("description")
        self.task2.pop("description")

        updated_tasks = self.__save_serializer(instance=self.tasks_to_update, data=[self.task, self.task2], many=True)["updated"]

        self.assertEqual(2,len(updated_tasks))
        self.assertEqual(self.task["name"],updated_tasks[0].name)
        self.assertEqual(self.task["name"],updated_tasks[1].name)
        self.assertEqual(self.tasks_to_update[0].description,updated_tasks[0].description)

    def test_update_multiple_tasks_no_name(self):

        self.task.pop("name")
        self.task2.pop("name")

        results = self.__save_serializer(instance=self.tasks_to_update, data=[self.task2,self.task], many=True)

        self.assertTrue(len(results["updated"])==0)

    def test_update_multiple_tasks_no_priority(self):
        
        self.task.pop("priority")
        self.task2.pop("priority")

        saved_tasks = self.__save_serializer(instance=self.tasks_to_update, data=[self.task2,self.task], many=True)["updated"]

        for saved_task in saved_tasks:
            self.assertIn(saved_task.priority,[Task.Priority.HIGH,Task.Priority.LOW], msg="priority value shouldn be changed for any of records")

    def test_update_multiple_tasks_no_deadline(self):
        
        self.task.pop("deadline")
        self.task2.pop("deadline")

        result = self.__save_serializer(instance=self.tasks_to_update, data=[self.task2,self.task], many=True)

        self.assertTrue(len(result["updated"])==0)
        self.assertTrue(len(result["errors"])==2)

    def test_update_multiple_tasks_no_authors(self):

        self.task.pop("authors")
        self.task2.pop("authors")

        result = self.__save_serializer(instance=self.tasks_to_update, data=[self.task2,self.task], many=True)

        self.assertTrue(len(result["updated"])==0)
        self.assertTrue(len(result["errors"])==2)    
        self.assertEqual(0, len(result["created"]))               

    def test_update_multiple_tasks_no_assigned_to(self):

        self.task.pop("assigned_to")
        self.task2.pop("assigned_to")

        saved_tasks = self.__save_serializer(instance=self.tasks_to_update, data=[self.task2,self.task], many=True)["updated"]

        self.assertEqual(2, len(saved_tasks))
    

    def test_update_multiple_tasks_one_task_invalid(self):
        
        task =  copy.deepcopy(self.task_test_data)
        task["id"] = self.id1
       
        task2 = copy.deepcopy(task)
        task.pop("name")
        task2["id"] = self.id2

        saved_tasks = self.__save_serializer(instance=self.tasks_to_update, data=[task,task2], many=True)

        updated_tasks = saved_tasks["updated"]
        errors_tasks = saved_tasks["errors"]


        self.assertEqual(1, len(updated_tasks))
        self.assertEqual(1, len(errors_tasks))
    

    def test_update_multiple_tasks_one_task_valid(self):

        valid_task = copy.deepcopy(self.task)

        invalid_task = copy.deepcopy(valid_task)
        invalid_task2 = copy.deepcopy(valid_task)

        invalid_task["name"] = ""

        invalid_task2.pop("authors")

        result = self.__save_serializer(instance=self.tasks_to_update, data = [invalid_task, invalid_task2, valid_task, invalid_task, invalid_task ], many=True)

        self.assertEqual(4,len(result["errors"]), msg="only one update must be executed, other 4 have to fail, be with errors")
        self.assertTrue(len(result["updated"])==1, msg="only one update must be executed, because only one valid task provided in test data")


    # def test_update_multiple_tasks_one_step_invalid(self):
    #     pass 

    # def test_update_multiple_tasks_one_step_valid(self):
    #     pass  