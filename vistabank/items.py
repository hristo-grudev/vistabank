import scrapy


class VistabankItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
