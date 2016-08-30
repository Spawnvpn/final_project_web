import json
import scrapy
import json
import re
# from scrapy.cmdline import execute
# execute()
from scrapy.shell import inspect_response


class InstagramImageSpider(scrapy.Spider):

    def __init__(self, req=None, **kwargs):
        super(InstagramImageSpider, self).__init__(**kwargs)
        self.req = req
    name = 'instagramimagespider'
    # req = 'cats'

    def start_requests(self):
        links = self.get_links()
        self.logger.info("LINKS: {}".format(", ".join(links)))
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        if not self.req:
            self.req = "cat"
        start_urls = ['https://www.instagram.com/explore/tags/%s/?__a=1' % self.req]
        return start_urls

    def parse(self, response):
        item = dict()
        # inspect_response(response, self)
        elements = response.xpath('//p/text()').extract()[0]
        elements = json.loads(elements)['tag']['media']['nodes']
        # self.logger.info(elements)
        for element in elements:
            image_url = element['thumbnail_src']
            self.logger.info(image_url)
            item['image_url'] = image_url
            item['search_engine'] = 'instagram'
            yield item
