from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UploadedFile

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'password', 'gender', 'fullname', 'public_visibility']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UploadedFile)
