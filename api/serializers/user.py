from rest_framework import serializers

from api.models import UserCustom
from api.serializers.customlistserializer import CustomListSerializer
# User Serializer

class UserSerializer(serializers.ModelSerializer):
    
    fullname = serializers.SerializerMethodField("get_fullname")

    def get_fullname(self, obj):
        return obj.get_full_name()
    
    class Meta:
        model = UserCustom
        fields = ['id', 'email', 'password', 'fullname']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }


class UserFullNameSerializer(UserSerializer):
    
    id = serializers.IntegerField(required=True)
    class Meta:
        model = UserCustom
        fields = ['id','fullname']
        list_serializer_class = CustomListSerializer
        
class LoggedUserDetailsSerializer(UserSerializer):
    
    class Meta:
        model = UserCustom
        exclude = ['password']
        
class UpdateUserDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserCustom
        fields = ['id','first_name', 'last_name', 'email', 'profile_picture','is_staff']
        extra_kwargs = {
            'first_name': {'required':True},
            'last_name': {'required':True},
            'email': {'required':True, 'read_only':True},
            'profile_picture':{'required':False},
        }