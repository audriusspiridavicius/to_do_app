from rest_framework import viewsets
from api.serializers.user import LoggedUserDetailsSerializer, UserSerializer
from django.contrib.auth import get_user_model
from api.models import UserCustom

User=get_user_model()

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    
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
        
        return super().get_serializer_class()
