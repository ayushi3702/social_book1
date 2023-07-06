from django.urls import path
from . import views
from .views import AuthorsSellersView
from page.views import upload_book, uploaded_files
from .views import send_email

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('authors-sellers/', AuthorsSellersView.as_view(), name='authors_sellers'),
    path('upload/', views.upload_book, name='upload_book'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),
    path('send-email/', views.send_email, name='send_email'),
]
