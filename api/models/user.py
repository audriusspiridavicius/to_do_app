from typing import Any, Iterable
import PIL.Image
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image
from io import BytesIO
class UserCustomManager(UserManager):
    
    use_in_migrations = True
    
    def create_user(self, email: str | None = ..., password: str | None = ..., **extra_fields: Any) -> Any:
        
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
        
    
    def create_superuser(self, email: str | None, password: str | None, **extra_fields: Any) -> Any:
        
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)
        



class UserCustom(AbstractUser):
    """Custom user model"""
    
    
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserCustomManager()
    profile_picture = models.ImageField(upload_to= "profile/", default="profile/default.png")


    def __str__(self):
        return self.email
    
    
    class Meta:
        
        db_table = "auth_user"
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def save(self, *args: Any, **kwargs: Any):
        
        super().save(*args, **kwargs)
        
        if self.profile_picture:
            img = Image.open(self.profile_picture.path).convert('RGB')
            img.thumbnail((100,100))
            img.save(self.profile_picture.path, quality=100)