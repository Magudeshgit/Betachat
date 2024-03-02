from django.shortcuts import render, redirect
from .forms import MakeUser, LogUser
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import boto3 as boto


def Home(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        email = send_mail(
        "BetaChat Feedback Form",
        content,
        settings.EMAIL_HOST_USER,
        ['magudesh2006@gmail.com'],
        fail_silently=False,
    ) 
    return render(request, 'authpages/index.html')

def Signin(request):
    if request.method == "POST":
        username=request.POST.get('username')
        passwd=request.POST.get('password')
        auth = authenticate(request,username=username,password=passwd)
        if auth is not None:
            login(request, auth)
            print('logged')
            return redirect('/')
        else:
           print('error')
           return render(request, 'authpages/Signin.html', {'error':'Your Username or password is incorrect'})
    return render(request, 'authpages/Signin.html')

def Signup(request):
    object = MakeUser()
    if request.method=='POST':
        object = MakeUser(request.POST)
        if object.is_valid():
            object.save()
            auth = authenticate(username=object.cleaned_data['username'],password=object.cleaned_data['password1'])
            login(request,auth)
            return redirect('/')
        else:
            print(object.errors)
            print('blah')
    return render(request, 'authpages/Signup.html', {'form': object})
    
def Logout(request):
    logout(request)
    return redirect('/')
