from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UploadedFile

# class CustomUser(admin.ModelAdmin):
#     list_display=('page image')

admin.site.register(CustomUser, UserAdmin)
admin.site.register(UploadedFile)
