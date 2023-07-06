from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django_filters.views import FilterView
from .filters import CustomUserFilter
from page.models import CustomUser, UploadedFile
from django.core.mail import send_mail

class AuthorsSellersView(FilterView):
    model = CustomUser
    template_name = 'authors_sellers.html'
    filterset_class = CustomUserFilter

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect('index')

        return HttpResponse('Invalid username or password')

    return render(request, 'login.html')


def logout(request):
    return render(request, 'logout.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def index(request):
    return render(request, 'index.html')

def upload_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        cost = request.POST.get('cost')
        year_published = request.POST.get('year_published')
        file = request.FILES['file']
        uploaded_file = UploadedFile(title=title, description=description, visibility=visibility, cost=cost, year_published=year_published, file=file)
        uploaded_file.save()
        return redirect('uploaded_files')

    return render(request, 'upload_book.html')

def uploaded_files(request):
    files = UploadedFile.objects.all()
    return render(request, 'uploaded_files.html', {'files': files})

def send_email(request):
    subject = 'Hello from Django'
    message = 'This is a test email sent using Django.'
    from_email = 'ayushipd02@gmail.com'  # Replace with the sender's email address
    recipient_list = ['praspd@gmail.com']  # Replace with the recipient's email address(es)

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # Optionally, you can also use the `html_message` parameter to send HTML content in the email.

    return HttpResponse('Email sent successfully.')
