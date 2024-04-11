
import string
from django.utils.timezone import make_aware 
from django.utils import timezone 
from django.utils import lorem_ipsum
from api.models import Step, Task
from django.contrib.auth import get_user_model
import random
User = get_user_model()

class TestSetUptestDatabase:

    def set_up_database(count = 10):

        
        user_list = [User.objects.create(username=f"username{index}",password=f"user{index}") for index in range(count)]
        
        step_list = [Step.objects.create(name=f"step number{index}") for index in range(count)]
        
        print(f"number of users created: {User.objects.count()}")
        print(f"number of steps created: {Step.objects.count()}")
        
        
        task_list = [
            {
                "name": f"Create registration functionality{index}",
                "description": lorem_ipsum.sentence(),
                "deadline": make_aware(timezone.datetime(2030,10,10)),
                "priority": Task.Priority.LOW,
                "assigned_to":User.objects.filter(id=random.choice(User.objects.all().values_list("id", flat=True)) ).first(),
            } for index in range(count)

            
        ]

        tasks = [Task.objects.create(**task) for task in task_list]

        [task.authors.set([random.choice(User.objects.all().values_list("id", flat=True))]) for task in tasks]
        tasks = [task.steps.set([1,random.choice(Step.objects.exclude(id=1).all().values_list("id", flat=True))]) for task in tasks]
         

        print(f"number of tasks created: {Task.objects.count()}")



