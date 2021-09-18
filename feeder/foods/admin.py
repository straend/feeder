from django.contrib import admin
from .models import Chain, Restaurant, Meal

# Register your models here.
admin.site.register(Chain)
admin.site.register(Restaurant)
#admin.site.register(Meal)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'date', 'food', 'price')
    list_filter = ('date', 'restaurant')
