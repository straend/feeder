## commands/crawl.py

from django.core.management.base import BaseCommand
from scraper.spiders.unica import UnicaSpider
from scraper.spiders.karkafeerna import KarkafeernaSpider
from scraper.spiders.sodexo import SodexoSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(SodexoSpider)
        process.crawl(UnicaSpider)
        process.crawl(KarkafeernaSpider)

        process.start()
