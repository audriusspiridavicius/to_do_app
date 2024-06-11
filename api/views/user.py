from rest_framework import viewsets
from api.serializers.user import LoggedUserDetailsSerializer, UpdateUserDetailsSerializer, UserSerializer
from django.contrib.auth import get_user_model
from api.models import UserCustom
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
User=get_user_model()

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet, viewsets.mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):

        users = UserCustom.objects.all()
        user_email = self.kwargs.get("email", None)
            
        if user_email:
            users = users.filter(email=user_email).all()
        return users

    def get_serializer_class(self):
        
        user_email = self.kwargs.get("email", None)
        
        if user_email:
            return LoggedUserDetailsSerializer
        
        if self.action == "update":
            self.serializer_class = UpdateUserDetailsSerializer
        
        
        return super().get_serializer_class()
