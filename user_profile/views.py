from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserSerializerDetail, CycleSerializer, CycleSerializerDetail, BoostSerializer, BoostSerializerDetail
from rest_framework import generics
from .models import MainCycle, Boost
from rest_framework.decorators import api_view
from rest_framework.response import Response

import services


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


@api_view(['GET'])
def callClick(request):
    data = services.clicker_services.call_click(request)
    return Response(data)

@api_view(['POST'])
def buyBoost(request):
    click_power, coins_count, level, price = services.clicker_services.buy_boost(request)
    return Response({'clickPower': click_power,
                     'coinsCount': coins_count,
                     'level': level,
                     'price': price})
