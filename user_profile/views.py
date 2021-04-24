from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .serializers import UserSerializer, UserDetailSerializer
from rest_framework import generics


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


def index(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        return HttpResponseRedirect('/notebook')
    else:
        return redirect('login')


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/notebook')
        else:
            return render(request, 'login.html', {'invalid': True})
    else:
        return render(request, 'login.html', {'invalid': False})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_notebook(request):
    return render(request, 'notebook.html', {})


def user_registration(request):
    data = {}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            data['res'] = 1
            return render(request, 'registration.html', data)
        else:
            form = UserCreationForm()
            data['res'] = -1
            data['form'] = form
            username = request.POST.get("username", "")
            if User.objects.filter(username=username).exists():
                data['usernameRegistered'] = True
            if not request.POST.get("password1", "") == request.POST.get("password2", ""):
                data['passwordsNotMatch'] = True
            return render(request, 'registration.html', data)
    else:
        form = UserCreationForm()
        data['res'] = 0
        data['form'] = form
        return render(request, 'registration.html', data)
