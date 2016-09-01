import json
import scrapy

from scrapy.loader import ItemLoader
from web_bot.items import ImageItem


class YandexImageSpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        super(YandexImageSpider, self).__init__(*args, **kwargs)
        self.keywords = kwargs.get('kwargs')
        self.job = kwargs.get('_job')
    name = 'yandeximagespider'

    def start_requests(self):
        links = self.get_links()
        self.logger.info("LINKS: {}".format(", ".join(links)))
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        if not self.keywords:
            self.keywords = ""
        self.keywords = self.keywords.replace(' ', '+')
        start_urls = ['https://yandex.ua/images/search?text=%s&rdpass=1' % self.keywords]
        return start_urls

    def parse(self, response):
        item_loader = ItemLoader(item=ImageItem(), response=response)
        image_list = list()
        # small_image_list = list()
        # origin_list = list()
        elements = response.xpath('//*[contains(@class, "serp-item_group_search")]').xpath('./@data-bem').extract()
        for element in elements:
            content = json.loads(element)['serp-item']['preview']
            image_list.append(content[0].get('url'))
            # origin_list.append(json.loads(element)['serp-item']['snippet']['domain'])
            # small_image_list.append(json.loads(element)['serp-item']['snippet']['url'])
        item_loader.add_value('image_url', image_list)
        # item_loader.add_value('small_images', small_image_list)
        item_loader.add_value('job_id', self.job)
        # item_loader.add_value('origin', origin_list)
        return item_loader.load_item()
