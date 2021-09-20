import scrapy
import json
import re
from datetime import datetime, date, timedelta
from foods.models import Restaurant, Chain, Meal
from ..items import MealItem


class SodexoSpider(scrapy.Spider):
    name = 'sodexo'
    start_urls = ['https://www.sodexo.fi/search/restaurants?search_api_fulltext=turku']

    def parse(self, response):
        restaurant_pages = response.css('div.region-content a::attr(href)').re('.*/ravintolat/.+')
        yield from response.follow_all(restaurant_pages, self.parse_restaurant_link)

    def parse_restaurant_link(self, response):
        r_name = response.css('div.header-title-wrapper h1 span::text').get()
        chain, _ = Chain.objects.get_or_create(
            name=self.name
        )
        restaurant, _ = Restaurant.objects.get_or_create(
            chain=chain,
            name=r_name
        )

        data = response.css('div#menuviewblock')
        for w in data.css('li'):
            date_str = w.css('a::text').get()
            ma = re.findall(r".+?(?P<date>\d{1,2})\.(?P<month>\d{1,2})", date_str)
            m_date = date.today()
            if ma:
                day, moth = ma[0]
                m_date = date(m_date.year, int(moth), int(day))
            else:
                continue
            Meal.objects.filter(restaurant=restaurant, date=m_date).delete()

            link = w.css('a::attr(href)').get()
            for m in data.css(link).css('div.mealrow'):
                f_title = m.css('p.meal-name::text').get()
                f_price = m.css('div.mealprices p::text')[0].get().split(' ')[0]
                f_diets = m.css('div.mealdietcodes span::text').getall()
                meal = MealItem()
                meal['restaurant'] = restaurant
                meal['date'] = m_date
                meal['food'] = "{} ({})".format(f_title, ", ".join(f_diets))
                meal['price'] = float(f_price.replace(',', '.'))
                yield meal

