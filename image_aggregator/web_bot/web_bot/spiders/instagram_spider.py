import scrapy
import json
from scrapy.shell import inspect_response


class InstagramImageSpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        super(InstagramImageSpider, self).__init__(*args, **kwargs)
        self.keywords = kwargs.get('kwargs')
        self.job = kwargs.get('_job')
    name = 'instagramimagespider'

    def start_requests(self):
        links = self.get_links()
        self.logger.info("LINKS: {}".format(", ".join(links)))
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        if not self.keywords:
            self.keywords = ""
        self.keywords = self.keywords.replace(' ', '+')
        start_urls = ['https://www.instagram.com/explore/tags/%s/?__a=1' % self.keywords]
        return start_urls

    def parse(self, response):
        item = dict()
        item['job_id'] = self.job
        # inspect_response(response, self)
        elements = response.xpath('//p/text()').extract()[0]
        elements = json.loads(elements)['tag']['media']['nodes']
        # self.logger.info(elements)
        for element in elements:
            image_url = element['thumbnail_src']
            item['image_url'] = image_url
            item['search_engine'] = 'instagram'
            yield item
