from rest_framework import viewsets
from api.serializers.user import UserSerializer
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


