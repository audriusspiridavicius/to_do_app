from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

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

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
        



class UserCustom(AbstractUser):
    """Custom user model"""
    
    
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserCustomManager()


    def __str__(self):
        return self.email
    
    
    class Meta:
        
        db_table = "auth_user"
        verbose_name = 'user'
        verbose_name_plural = 'users'
        