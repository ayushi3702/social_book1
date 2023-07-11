from django.urls import include, path
from . import views
# from .views import AuthorsSellersView
from page.views import upload_book, uploaded_files, authors_sellers
from .views import send_email

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    # path('authors-sellers/', AuthorsSellersView.as_view(), name='authors_sellers'),
    path('upload/', views.upload_book, name='upload_book'),
    path('uploaded_files/', views.uploaded_files, name='uploaded_files'),
    path('send-email/', views.send_email, name='send_email'),
    path('authors-sellers/', views.authors_sellers, name='authors_sellers'),
    path('my_books_wrapper', views.my_books_wrapper, name="my_books_wrapper"),
    path('verify/', views.verify, name='verify'),
    path('activate/<str:activation>/', views.activate, name='activate'),
]
