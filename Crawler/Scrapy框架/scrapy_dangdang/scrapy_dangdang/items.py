# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # title = scrapy.Field()
    src = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
