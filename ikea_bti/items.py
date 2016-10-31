# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IkeaBtiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    family_price = scrapy.Field()
    package_price = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
