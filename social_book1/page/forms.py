from django import forms
from .models import CustomUser, UploadedFile
from django.contrib.auth.hashers import make_password

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'gender', 'fullname')

    def save(self, commit=True):
        instance = super().save(commit=False)
        pwd = self.cleaned_data['password']
        pwd = make_password(pwd)
        instance.password = pwd
        if commit:
            instance.save()
        return instance

class UploadedFile(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('title', 'description', 'visibility', 'cost', 'year_published')
