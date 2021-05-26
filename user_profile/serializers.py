from rest_framework import serializers
from .models import User, MainCycle, Boost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'cycle']


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id']


class CycleSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id', 'user', 'coinsCount', 'clickPower', 'boosts']


class BoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = ['id', 'boost_id', 'level', 'power', 'price']


class BoostSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = ['id', 'boost_id', 'level', 'power', 'price']
