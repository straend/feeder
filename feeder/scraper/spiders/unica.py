import scrapy
import json
import re
from datetime import datetime, date
from foods.models import Restaurant, Chain, Meal
from ..items import MealItem


class UnicaSpider(scrapy.Spider):
    name = 'unica'
    start_urls = ['https://www.unica.fi/ravintolat/']

    def parse(self, response):
        restaurant_pages = response.css('a::attr(href)').re('.*/ravintolat/.+')
        yield from response.follow_all(restaurant_pages, self.parse_restaurant_link)

    def parse_restaurant_link(self, response):
        json_links = response.css('a::attr(href)').re('.*json.*')
        if len(json_links) > 0:
            json_url = response.css('a::attr(href)').re('.*json.*')[0]
            yield scrapy.Request(response.urljoin(json_url), self.parse_json)

    def parse_json(self, response):
        data = json.loads(response.text)
        r_name = data['RestaurantName']
        chain, _ = Chain.objects.get_or_create(
            name=self.name
        )
        restaurant, _ = Restaurant.objects.get_or_create(
            chain=chain,
            name=r_name
        )
        food_re = re.compile(r"(?P<Food>.+)\((?P<Allergens>.+(?=\)))")

        for d in data['MenusForDays']:
            f_date = d['Date']
            m_date = date.fromisoformat(f_date.split('T')[0])
            # Get rid of old meals for today
            Meal.objects.filter(restaurant=restaurant, date=m_date).delete()

            if len(d['SetMenus']) == 0:
                continue
            for m in d['SetMenus']:
                if m['Price'] is None:
                    continue
                f_price = m['Price'].split("/")[0].strip()
                meal = MealItem()
                meal['restaurant'] = restaurant
                meal['date'] = m_date
                meal['food'] = "\n".join(m['Components'])
                meal['price'] = float(f_price.replace(',', '.'))
                yield meal
