import json
import scrapy
# from scrapy.cmdline import execute
# execute()
from scrapy.shell import inspect_response


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
        item = dict()
        item['job_id'] = self.job
        # inspect_response(response, self)
        elements = response.xpath('//*[contains(@class, "serp-item_group_search")]').xpath('./@data-bem').extract()
        for element in elements:
            content = json.loads(element)['serp-item']['preview']
            content = content[0].get('url')
            origin = json.loads(element)['serp-item']['snippet']['domain']
            small_image = json.loads(element)['serp-item']['snippet']['url']
            image_url = content
            item['origin'] = origin
            item['image'] = small_image
            item['image_url'] = image_url
            item['search_engine'] = 'yandex.ua'
            yield item
