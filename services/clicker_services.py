from django.contrib.auth.models import User
from user_profile.models import MainCycle, Boost
from user_profile.serializers import BoostSerializer


def main_page(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        mainCycle = MainCycle.objects.get(user=request.user)
        return (False, 'index.html', {'user':user[0], 'mainCycle':mainCycle})
    else:
        return (True, 'login', {})


def call_click(request):
    user = User.objects.filter(id=request.user.id)
    mainCycle = MainCycle.objects.filter(user=request.user)[0]

    is_level_up = mainCycle.Click()
    boosts_query = Boost.objects.filter(mainCycle=mainCycle)
    boosts = BoostSerializer(boosts_query, many=True).data

    mainCycle.save()
    return ({"coinsCount": mainCycle.coinsCount, "boosts": boosts})


def buy_boost(request):
    boost_id = request.data['boost_id']
    cycle = MainCycle.objects.filter(user=request.user)[0]
    boost = Boost.objects.get_or_create(mainCycle=cycle, boost_id=boost_id)[0]
    if cycle.coinsCount >= boost.price:
        click_power, coins_count, level, price = boost.Upgrade()
    boost.save()
    return (click_power, coins_count, level, price)