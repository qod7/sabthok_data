# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# Item description for gsmarena
class GsmareanaItem(scrapy.Item):
    Name = scrapy.Field()
    Network = scrapy.Field()
    Launch = scrapy.Field()
    Body = scrapy.Field()
    Display = scrapy.Field()
    Platform = scrapy.Field()
    Memory = scrapy.Field()
    Camera = scrapy.Field()
    Sound = scrapy.Field()
    Comms = scrapy.Field()
    Features = scrapy.Field()
    Battery = scrapy.Field()
    Misc = scrapy.Field()
    Tests = scrapy.Field()
