from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email=None, password=None, fullname=None, dob=None, age=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, fullname=fullname, dob=dob, age=age, **extra_fields)

    def _create_user(self, username, email, password=None, fullname=None, dob=None, age=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set.')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        # Hash the password
        if password:
            password = make_password(password)

        # Create and save the user
        user = self.model(username=username, email=email, fullname=fullname, dob=dob, age=age, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    fullname = models.CharField(max_length=255)
    public_visibility = models.BooleanField(default=False)
    # today = date.today().year
    # dob = models.IntegerField(
    #     validators=[
    #         MaxValueValidator(2023, message='Number should be maximum 4 digits.'),
    #         MinValueValidator(2023, message='Number should be minimum 0.'),
    #     ]
    # )
    # objects = CustomUserManager()

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         return super().save(*args, **kwargs)

class UploadedFile(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(default='N/A')
    visibility = models.CharField(max_length=100, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=300)
    year_published = models.IntegerField(default=datetime.now().year)
    file = models.FileField(upload_to='uploads/', null=True)

page_image = models.FileField(upload_to="page/", max_length=250, null=True, default=None)

# Any additional fields or methods specific to your user model

def __str__(self):
    return self.username
