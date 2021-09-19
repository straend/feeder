from django.shortcuts import render
from django.template import loader

import datetime
from .models import Meal, Restaurant
from django.urls import reverse

def today(request, day=None, month=None, year=None):
    now = datetime.date.today()

    if day is None:
        day = now.day
    if month is None:
        month = now.month
    if year is None:
        year = now.year
    d = datetime.date(year, month, day)
    meals = Meal.objects.filter(date=d)
    mm = {}
    for m in meals:
        if m.restaurant.name in mm:
            mm[m.restaurant.name].append(m)
        else:
            mm[m.restaurant.name] = [m]
    prev = d - datetime.timedelta(days=1)
    next = d + datetime.timedelta(days=1)

    context = {
        'date': d,
        'mm': mm,
        'prev_url': prev.strftime("%d/%m/%Y"),
        'next_url': next.strftime("%d/%m/%Y"),

    }

    return render(request, 'today.html', context)