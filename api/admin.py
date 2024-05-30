from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from django.http.response import HttpResponse
from api.models.user import UserCustom
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext as _
# Register your models here.
@admin.register(UserCustom)

class UserCustomAdmin(UserAdmin):
   ordering = ['email']
   list_display = ['id','email', 'first_name', 'last_name']
   list_display_links = ['email']
   fieldsets = (
      (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
      (
         _("Permissions"),
         {
               "fields": (
                  "is_active",
                  "is_staff",
                  "is_superuser",
                  "groups",
                  "user_permissions",
               ),
         },
      ),
      (_("Important dates"), {"fields": ("last_login", "date_joined")}),
   )
   add_fieldsets = (
      (
         None,
         {
               "classes": ("wide",),
               "fields": ("email", "password1", "password2"),
         },
      ),
   )

   def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
      if obj:
         return ['email']
      return super().get_readonly_fields(request, obj)