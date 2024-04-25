from django.urls import include, path
from rest_framework import routers
from api import views
# from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'steps', views.StepViewSet, basename="step")
router.register(r'tasks', views.TaskViewSet, basename="task")
router.register(r'users', views.UserViewSet, basename="user")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    
    path("tasks/name/<str:taskname>/", views.TaskViewSet.as_view({"get":"list"}), name="task-filter-name"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]