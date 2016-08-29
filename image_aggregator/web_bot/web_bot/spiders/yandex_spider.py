import json
import scrapy
# from scrapy.cmdline import execute
# execute()
from scrapy.shell import inspect_response


class YandexImageSpider(scrapy.Spider):

    def __init__(self, req=None, **kwargs):
        super(YandexImageSpider, self).__init__(**kwargs)
        self.req = req
    name = 'yandeximagespider'
    # req = 'cats'

    def start_requests(self):
        links = self.get_links()
        self.logger.info("LINKS: {}".format(", ".join(links)))
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        if not self.req:
            self.req = "ocean"
        start_urls = ['https://yandex.ua/images/search?text=' + self.req + '&rdpass=1']
        return start_urls

    def parse(self, response):
        item = dict()
        # inspect_response(response, self)
        elements = response.xpath('//*[contains(@class, "serp-item_group_search")]').xpath('./@data-bem').extract()
        for element in elements:
            content = json.loads(element)['serp-item']['preview']
            content = content[0].get('url')
            origin = json.loads(element)['serp-item']['snippet']['domain']
            self.logger.info(content)
            small_image = json.loads(element)['serp-item']['snippet']['url']
            image_url = content
            self.logger.info(content)
            item['origin'] = origin
            item['image'] = small_image
            item['image_url'] = image_url
            item['search_engine'] = 'yandex.ua'
            yield item
