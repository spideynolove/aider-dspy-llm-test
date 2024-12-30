import scrapy

class FinancialDataItem(scrapy.Item):
    _id = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()
    timestamp = scrapy.Field()
