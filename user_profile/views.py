from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .serializers import UserSerializer, UserSerializerDetail, CycleSerializer, CycleSerializerDetail, BoostSerializer, BoostSerializerDetail
from rest_framework import generics
from .models import MainCycle, Boost


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail


class CycleList(generics.ListAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializer


class CycleDetail(generics.RetrieveAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = CycleSerializerDetail


class BoostList(generics.ListAPIView):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer


class BoostDetail(generics.RetrieveAPIView):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializerDetail


def callClick(request):
    user = User.objects.filter(id=request.user.id)
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    mainCycle.Click()
    mainCycle.save()
    return HttpResponse(mainCycle.coinsCount)


def buyBoost(request):
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    if len(Boost.objects.filter(mainCycle=mainCycle)) == 0:
        if mainCycle.coinsCount < 10:
            return HttpResponse(mainCycle.clickPower)
        boost = Boost()
        boost.mainCycle = mainCycle
        boost.Upgrade()
        boost.save()
    else:
        boost = Boost.objects.filter(mainCycle=mainCycle)[0]
        if mainCycle.coinsCount < boost.price:
            return HttpResponse(mainCycle.clickPower)
        boost.mainCycle = mainCycle
        boost.Upgrade()
        boost.save()
    mainCycle.save()
    return HttpResponse(mainCycle.clickPower)
