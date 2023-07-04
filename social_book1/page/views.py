# Create your views here.
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'home.html')

def registeruser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Error Occured')

    context = {'form': form}
    return render(request, 'register.html', context)

def loginuser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid username or password')

    context = {'page': page}
    return render(request, 'login.html', context)

def logoutuser(request):
    logout(request)
    return redirect('home')
