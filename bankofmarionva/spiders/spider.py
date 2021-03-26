import scrapy

from scrapy.loader import ItemLoader

from ..items import BankofmarionvaItem
from itemloaders.processors import TakeFirst


class BankofmarionvaSpider(scrapy.Spider):
	name = 'bankofmarionva'
	start_urls = ['https://www.bankofmarionva.com/news']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class,"row two-col")]')
		for post in post_links:
			title = post.xpath('.//strong/text()').get()
			description = post.xpath('.//p//text()[normalize-space() and not(ancestor::p[strong])]').getall()
			description = [p.strip() for p in description]
			description = ' '.join(description).strip()
			date = post.xpath('.//em/text()').get()

			item = ItemLoader(item=BankofmarionvaItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
