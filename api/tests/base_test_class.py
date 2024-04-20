from dataclasses import dataclass, field
from django.db.models import Model
from rest_framework.serializers import Serializer
from typing import Any
from django.core.exceptions import ValidationError


@dataclass
class BaseTestClass:
    serializer_class: Serializer 
    model_class: Model  

    def save_serializer(self,data,print_errors = False, *args, **kwargs) -> Any | list:
        
        serializer = self.serializer_class(data=data,*args, **kwargs)
        if serializer.is_valid():
        
            saved_model_data = serializer.save()

            return saved_model_data
        
        else:
            if print_errors: print(f" ValidationError occured => {serializer.errors}") 
            raise ValidationError(message=f"serializer {self.serializer_class} is not valid. error = {serializer.errors}")
