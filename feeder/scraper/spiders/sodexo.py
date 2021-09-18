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
        json_links = response.css('a::attr(href)').re('.*weekly_json.*')
        # Keep only one of each link
        json_links = list(set(json_links))
        for json_url in json_links:
            yield scrapy.Request(response.urljoin(json_url), self.parse_json)

    def parse_json(self, response):
        data = json.loads(response.text)
        r_name = data['meta']['ref_title']
        chain, _ = Chain.objects.get_or_create(
            name=self.name
        )
        restaurant, _ = Restaurant.objects.get_or_create(
            chain=chain,
            name=r_name
        )
        date_re = re.compile(r"(?P<start_d>\d+)\.(?P<start_m>\d+)\.")
        rm = date_re.findall(data['timeperiod'])
        start_date = None
        if rm:
            day, month = rm[0]
            year = datetime.now().year
            start_date = date(year, int(month), int(day))
        else:
            return
        for i, d in enumerate(data['mealdates']):
            m_date = start_date + timedelta(days=i)
            Meal.objects.filter(restaurant=restaurant, date=m_date).delete()
            if len(d['courses']) == 0:
                continue
            for m_i in d['courses']:
                m = d['courses'][m_i]
                f_price = m['price'].split('€')[0].strip() if 'price' in m else '0.0'
                meal = MealItem()
                meal['restaurant'] = restaurant
                meal['date'] = m_date
                meal['food'] = "{} ({})".format(m['title_fi'], m['dietcodes'] if 'dietcodes' in m else '')
                meal['price'] = float(f_price.replace(',', '.'))
                yield meal
