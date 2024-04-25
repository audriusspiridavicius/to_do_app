from rest_framework import serializers
from django.contrib.auth.models import User

# User Serializer

class UserSerializer(serializers.ModelSerializer):
    
    fullname = serializers.SerializerMethodField("get_fullname")

    def get_fullname(self, obj):
        return obj.get_full_name()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'fullname']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
            'email': {'required': True}
        }


class UserFullNameSerializer(UserSerializer):
    
    class Meta:
        model = User
        fields = ['id','fullname']