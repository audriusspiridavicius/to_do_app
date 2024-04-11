from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from api.models.step import Step
from api.tests.set_up_database import TestSetUptestDatabase
from api.serializers.step import StepSerializer
from api.views.step import StepViewSet
class TestStepViewset(TestCase, TestSetUptestDatabase):

    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.data_count = 20

        cls.set_up_database(cls.data_count)

        return super().setUpTestData()
    
    def test_get_step_list(self):
        """check if steps list is available"""
        response = self.client.get(reverse("step-list"))
 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.data_count, Step.objects.count())
        self.assertEqual(self.data_count, len(response.json()))

    def test_get_step_detail(self):
        """check step detail page is available"""
        id = 5

        response = self.client.get(reverse("step-detail",args=[id]))

        self.assertEqual(id,response.json()["id"])

    def test_get_non_existing_step_detail(self):
        """try to get non existing step data"""

        id = self.data_count + 10

        response = self.client.get(reverse("step-detail",args=[id]))

        self.assertEqual(status.HTTP_404_NOT_FOUND,response.status_code)

    def test_create_new_step(self):
        """create new step using valid data and without tasks assigned"""

        data = {"name": "very important and urgent assignment is going on here"}
        response = self.client.post(reverse("step-list"), data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.data_count+1,Step.objects.count())

    def test_create_new_step_with_task(self):
        """create new step using valid data and with task assigned"""

        task_number = 5
        data = {"name": "very important and urgent assignment is going on here", "tasks":[number for number in range(1,task_number+1)]}
        response = self.client.post(reverse("step-list"), data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.data_count+1,Step.objects.count())
        self.assertEqual(task_number,Step.objects.filter(id=response.json()["id"]).first().tasks.all().count())

    def test_extra_action(self):
        """get extra action data"""

        response = self.client.get(reverse("step-step_tasks"))

        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=" extra action data list should be returned")