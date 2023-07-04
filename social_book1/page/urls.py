from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registeruser, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('', views.home, name="login_user"),
]
