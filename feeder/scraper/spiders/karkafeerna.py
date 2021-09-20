import scrapy

from datetime import datetime, date, timedelta
from foods.models import Restaurant, Chain, Meal
from ..items import MealItem


class KarkafeernaSpider(scrapy.Spider):
    name = 'karkafeerna'
    allowed_domains = ['www.karkafeerna.fi']
    start_urls = ['http://www.karkafeerna.fi/se']

    def parse(self, response):
        restaurant_pages = response.css('a::attr(href)').re('.*veckans-lista.*')
        yield from response.follow_all(restaurant_pages, self.parse_weeks)

    def parse_weeks(self, response):
        restaurant_pages = response.css('a::attr(href)').re('.*veckans-lista.*')
        yield from response.follow_all(restaurant_pages, self.parse_restaurant)

    def parse_restaurant(self, response):
        price_groups = {1: 4.5, 2: 2.7, 3: 2.7, 4: 2.4, 5: 2.7, 6: 2.0 }
        allergens = {'G': 'Gluten free', 'M': 'Milk free',
                     'C': 'Contains citrus fruit', 'P': 'Contains Paprika/Chili',
                     'Vgn': 'Vegan', 'Ä': 'Contains eggs', 'S': 'Contains Celery'}
        x = response.css('div.meals')
        days = x.css('h3.day-row::text')
        days_data = x.css('div.week-list')

        restaurant = response.css('img::attr(alt)').get()
        chain, _ = Chain.objects.get_or_create(
            name=self.name
        )
        restaurant, _ = Restaurant.objects.get_or_create(
            chain=chain,
            name=restaurant
        )

        for (d, data) in zip(days, days_data):
            dat = d.get().split(" ")[1]
            m_date = datetime.strptime(dat, "%d.%m.%Y").date()

            # Get rid of old meals for today
            Meal.objects.filter(restaurant=restaurant, date=m_date).delete()

            for x in data.css('div.meal'):
                f_title = x.css('span.food::text').get().strip()
                f_price = int(x.css('span.price-group::text').get())
                f_allergens = x.css('span.food-diet::text').getall()
                meal = MealItem()
                meal['restaurant'] = restaurant
                meal['date'] = m_date
                meal['food'] = "{} ({})".format(f_title, ",".join(f_allergens))
                meal['price'] = price_groups[f_price]
                yield meal
