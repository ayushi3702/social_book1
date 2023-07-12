from math import floor
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django_filters.views import FilterView
from .filters import CustomUserFilter
from page.models import CustomUser, UploadedFile
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from page.wrapper import my_books_wrapper
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.conf import settings
import string

# class AuthorsSellersView(FilterView):
#     model = CustomUser
#     template_name = 'authors_sellers.html'
#     filterset_class = CustomUserFilter

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
                # auth_login(request, user)
                # return redirect('index')
                otp_token = send_otp(request, user)
                request.session['otp'] = otp_token
                request.session["username"] = username
                request.session["password"] = password
                return redirect("verify")
        return render(request, "login.html", {"error_message": "Invalid username or password"})
    return render(request, "login.html")

#  return HttpResponse('Invalid username or password')

# return render(request, 'login.html')

@login_required(login_url="login")
def logout(request):
    auth_logout(request)
    return redirect("")

# # def register(request):
# #     if request.method == 'POST':
# #         form = CustomUserCreationForm(request.POST)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('index')
# #     else:
# #         form = CustomUserCreationForm()

#     return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        fullname = request.POST.get("fullname")
        global global_key, name
        print(fullname)
        email = request.POST.get("email")
        print(email)
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        print(password)
        print(username)
        request.session['username'] = username
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activation_key = generate_activation_key()
            print(activation_key)
            global_key = activation_key
            print(global_key)
            name = username
            # request.session['key'] = activation_key
            # print(request.session.get('key'))
            subject = 'Social Book Registration'
            message = f'Hello {fullname}, You have been registered with us successfully. Please verify your email by clicking on this link: http://localhost:8000/activate/{activation_key}/'
            from_email = settings.EMAIL_HOST_USER
            to_email = email
            print(to_email)
            send_mail(subject, message, from_email, [to_email])
            print(subject, message, from_email, [to_email])
            return render(request, 'login.html')
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def generate_otp():
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[floor(random.random() * 10)]
    return otp

def generate_activation_key():
    chars = string.ascii_letters + string.digits
    activation_key = ''.join(random.choice(chars) for _ in range(16))
    return activation_key

@login_required(login_url="login")
def index(request):
    print(request.user.fullname)
    return render(request, "index.html", {"user": request.user})

# def index(request):
#     return render(request, 'index.html')

# @login_required(login_url="login")
# def authors_sellers(request):
#     users = CustomUser.objects.filter(public_visibility=True)
#     print(users)
#     files = UploadedFile.objects.all()
#     print(files)
#     # files = files.filter(visibility=True)
#     files_per_user = {}
#     for user in users:
#         files_per_user[user.username] = files.filter(
#             visibility=True, username=user.username
#         )
#         print(files_per_user)
#     # for user in users:
#     #     for username, file in files_per_user.items():
#     #         if user.username == username:
#     #             for f in file:
#     #                 print(f.file.url)
#     return render(request, "filter.html", {"users": users, "files": files_per_user})

@login_required(login_url="login")
def upload_file(request):
    if request.user.is_authenticated:
        username = request.user.username

    if request.method == "POST":
        form = UploadedFile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UploadedFile()
    return render(request, "upload_files.html", {"form": form, "username": username})

def authors_sellers(request):
    users = CustomUser.objects.filter(public_visibility=True).all()
    return render(request, 'authors_sellers.html', {'users': users})

def upload_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        cost = request.POST.get('cost')
        year_published = request.POST.get('year_published')
        file = request.FILES['file']
        username = request.POST.get('username')
        uploaded_file = UploadedFile(title=title, description=description, visibility=visibility, cost=cost, year_published=year_published, file=file, username=username)
        uploaded_file.save()
        return redirect('uploaded_files')

    return render(request, 'upload_book.html')

# @login_required(login_url="login")
# def uploaded_files(request):
#     if request.user.is_authenticated:
#         # username = request.user.username
#         # print(username)
#         files = UploadedFile.objects.all()
#         files = files.filter(visibility=True)
#         # if username is not None:
#         #     files = files.filter(username=username)
#         for file in files:
#             print(file.file.url)
#     return render(request, "uploaded_files.html", {"files": files})

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

class TokenCreateView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uploaded_file(request, file_id):
    try:
        file = UploadedFile.objects.get(title=file_id)
        # Perform any additional logic here if needed
        return Response({'file_url': file.file.url})
    except UploadedFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=404)

@my_books_wrapper
def my_books_wrapper(request):
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        file = UploadedFile.objects.filter(username=username).all()
        print(file)
        # if file is not None:
        return render(request, 'uploaded_files.html', {'files': file})

# def otp_login_view(request):
#     return render(request, 'otp_login.html')

# @login_required
# def otp_verify_view(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         # Perform OTP verification logic
#         if otp_is_valid:
#             # OTP is valid, continue with the authentication process
#             return redirect('dashboard')
#         else:
#             # Invalid OTP, display error message or redirect to login
#             return redirect('login')
#     else:
#         return render(request, 'otp_verify.html')

def verify(request):
    otp_token = request.session.get('otp')
    password = request.session.get('password')
    username = request.session.get('username')
    if request.method == 'POST':
        token = request.POST.get('token')
        print(token)
        print(otp_token)
        if str(token) == str(otp_token):
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            return redirect('index')
        return render(request, 'login.html', {"error_message": "OTP verification failed due to mismatch OTP"})
    return render(request, 'verify.html')

def activate(request, activation):
    global global_key, name
    key = global_key
    print(request.session.get('key'))
    print("key got from session: ", key)
    print("Activation Key got from user:", activation)
    username = name
    print(username)
    if str(activation) == str(key):
        user = CustomUser.objects.get(username=username)
        print(user.is_active)
        user.is_active = True
        user.save()
        print(user.is_active)
        print("Activation Successful")
        return redirect('login')
    else:
        return HttpResponse("Email Verfication Failed")

def send_otp(request, user):
    otp_token = generate_otp()
    print(otp_token)
    subject = 'Social Book Login OTP'
    message = f'Hello {user.username}, Your OTP is: {otp_token}.'
    from_email = settings.EMAIL_HOST_USER
    to_email = user.email
    print(to_email)
    send_mail(subject, message, from_email, [to_email])
    print(subject, message, from_email, [to_email])
    return otp_token

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        global global_email, global_key
        global_email = email
        reset_key = generate_activation_key()
        global_key = reset_key
        link = f"http://localhost:8000/reset_password/{reset_key}"
        from_email = settings.EMAIL_HOST_USER
        send_mail("Forget link", link, from_email, [email])
        print("Forget link", link, from_email, [email])
        return redirect("login")
    return render(request, "forgot_password.html")

def resetpassword(request, reset_key):
    global global_email, global_key
    # print(global_email, global_key)
    print('1')
    if request.method == 'POST':
        print('2')
        p1 = request.POST.get('passwordone')
        p2 = request.POST.get('passwordtwo')
        if str(p1) == str(p2):
            user = CustomUser.objects.get(email=global_email)
            print(user)
            user.password = make_password(p1)
            user.save()
            return redirect('login')
    return render(request, "reset_password.html")

# def forgotpassword(request):
#     try:
#         if request.method == 'POST':
#             username = request.POST.get('username')

#             if not User.objects.filter(username=username).first():
#                 messages.success(request, 'No User Found with this username')
#                 return redirect('/forgot-password/')
#             user_obj = User.objects.get(username=username)

# def forgotpassword(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user = CustomUser.objects.get(email=email)
#         token = user.token

# def resetpassword(request, token):
#     user = get_object_or_404(CustomUser, token=token)
#     if request.method == 'POST':
#         new_password = request.POST.get("password")
#         user.password = make_password(new_password)
#         print(new_password)
#         print(user.password)
#         user.save()
#         return render(request, 'login')
#     return render(request, 'reset_password.html')
