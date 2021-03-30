import scrapy

from scrapy.loader import ItemLoader

from ..items import VistabankItem
from itemloaders.processors import TakeFirst


class VistabankSpider(scrapy.Spider):
	name = 'vistabank'
	start_urls = ['https://www.vistabank.com/newsroom']

	def parse(self, response):
		post_links = response.xpath('//a[@data-category="recognition"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[2]//text()[normalize-space()]').get()
		description = response.xpath('//div[@class="hhs-rich-text c1"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=VistabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
