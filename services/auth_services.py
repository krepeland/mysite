from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from user_profile.models import MainCycle


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return (True, 'index', {})
        else:
            return (False, 'login.html', {'invalid':True})
    else:
        return (False, 'login.html', {'invalid':False})


def user_logout(request):
    logout(request)
    return ('login')


def user_registration(request):
    data = {}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            mainCycle = MainCycle()
            mainCycle.user = user
            mainCycle.save()

            data['res'] = 1
            return (False, 'registration.html', data)
        else:
            form = UserCreationForm()
            data['res'] = -1
            data['form'] = form
            username = request.POST.get("username", "")
            if User.objects.filter(username=username).exists():
                data['usernameRegistered'] = True
            if not request.POST.get("password1", "") == request.POST.get("password2", ""):
                data['passwordsNotMatch'] = True
            return (False, 'registration.html', data)
    else:
        form = UserCreationForm()
        data['res'] = 0
        data['form'] = form
        return (False, 'registration.html', data)