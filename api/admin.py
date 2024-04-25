from django.contrib import admin
from api.models.user import UserCustom
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(UserCustom)
class UserCustomAdmin(UserAdmin):
   ordering = ['email']