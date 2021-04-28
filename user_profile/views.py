from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .serializers import UserSerializer, UserDetailSerializer
from rest_framework import generics
from .models import MainCycle


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


def callClick(request):
    user = User.objects.filter(id=request.user.id)
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    mainCycle.Click()
    mainCycle.save()
    return HttpResponse(mainCycle.coinsCount)
