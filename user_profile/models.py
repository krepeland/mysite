from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class MainCycle(models.Model):
    user = models.OneToOneField(User, related_name='cycle', null=False, on_delete=models.CASCADE)

    coinsCount = models.IntegerField(default=0)
    clickPower = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    def set_main_cycle(self, coinsCount):
        self.coinsCount = coinsCount
        return self.check_level()

    def check_level(self):
        if self.coinsCount > (self.level**4)*100:
            boost_type = 0
            if self.level % 3 == 0:
                boost_type = 1

            if self.level == 0:
                boost = Boost(mainCycle=self, boost_id=self.level, price=10, power=1,  boost_type=boost_type, level_cost=5)
                boost.save()
            else:
                boost = Boost(mainCycle=self, boost_id=self.level, price=(self.level**4)*125, power=int(((self.level+1)**3)/1.5 * (1+boost_type*4)),  boost_type=boost_type, level_cost=(self.level**4)*5)
                boost.save()
            self.level += 1
            self.save()
            return True
        return False


class Boost(models.Model):
    mainCycle = models.ForeignKey(MainCycle, related_name='boosts', null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=1)
    level = models.IntegerField(default=0, null=False)
    boost_id = models.IntegerField(default=0, null=False)
    price = models.IntegerField(default=10)
    level_cost = models.IntegerField(default=5)
    boost_type = models.IntegerField(default=1)

    def Upgrade(self):
        self.level += 1

        if self.boost_type == 0:
            self.mainCycle.clickPower += self.power
        else:
            self.mainCycle.auto_click_power += self.power
        self.mainCycle.coinsCount -= self.price
        self.mainCycle.save()

        self.price += self.level_cost * self.level

        return (self.mainCycle.clickPower, self.mainCycle.coinsCount, self.level, self.price)


    def update_coins_count(self, current_coins_count):
        self.mainCycle.coinsCount += current_coins_count
        return self.mainCycle