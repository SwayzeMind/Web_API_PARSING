import scrapy

class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    salary = scrapy.Field()