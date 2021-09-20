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
    meals = Meal.objects.prefetch_related('restaurant').filter(date=d)

    # Sort in Alphabetical order, kinda hacky
    mm = {}
    for m in meals:
        if m.restaurant.name in mm:
            mm[m.restaurant.name].append(m)
        else:
            mm[m.restaurant.name] = [m]
    prev_d = d - datetime.timedelta(days=1)
    next_d = d + datetime.timedelta(days=1)
    mmm = {x: mm[x] for x in sorted(mm)}

    context = {
        'date': d,
        'mm': mmm,
        'prev_url': prev_d.strftime("%d/%m/%Y"),
        'next_url': next_d.strftime("%d/%m/%Y"),

    }

    return render(request, 'today.html', context)