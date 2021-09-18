# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from foods.models import Restaurant, Chain, Meal


class MealItem(DjangoItem):
    django_model = Meal


class FeedmeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
