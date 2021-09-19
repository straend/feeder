import datetime

from django.db import models


class Chain(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    chain = models.ForeignKey(Chain, on_delete=models.PROTECT, related_name='restaurants')

    @property
    def has_today(self):
        return len(self.meals.filter(date=datetime.datetime.now().date())) > 0

    @property
    def today(self):
        return self.meals.filter(date=datetime.datetime.now().date())

    def __str__(self):
        return "{}: {}".format(self.chain, self.name)


class Meal(models.Model):
    price = models.DecimalField(max_digits=4, decimal_places=2)
    food = models.CharField(max_length=512)
    date = models.DateField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='meals')

    def __str__(self):
        return "{}".format(self.food[:60])