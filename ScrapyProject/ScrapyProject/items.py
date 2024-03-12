# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AvitoItem(scrapy.Item):
    name = scrapy.Field()
    url_offer = scrapy.Field()
    price = scrapy.Field()
    ville = scrapy.Field()
    type = scrapy.Field()
    secteur = scrapy.Field()
    surface_habitable = scrapy.Field()


class MubawabItem(scrapy.Item):
    name = scrapy.Field()
    url_offer = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field()
    secteur_et_ville = scrapy.Field()
    surface = scrapy.Field()
