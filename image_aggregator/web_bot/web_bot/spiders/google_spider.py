import json
import scrapy
from scrapy.shell import inspect_response


class GoogleImageSpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        super(GoogleImageSpider, self).__init__(*args, **kwargs)
        self.keywords = kwargs.get('kwargs')
        self.job = kwargs.get('_job')
        self.logger.info(self.keywords)
    name = 'googleimagespider'

    def start_requests(self):
        links = self.get_links()
        self.logger.info("LINKS: {}".format(", ".join(links)))
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        if not self.keywords:
            self.keywords = "cats"
        self.keywords = self.keywords.replace(' ', '+')
        start_urls = ['https://www.google.com.ua/search?q=%s&source=lnms&tbm=isch' % self.keywords]
        return start_urls

    def parse(self, response):
        item = dict()
        item['job_id'] = self.job
        # inspect_response(response, self)
        elements = response.xpath('//*[@id="rg_s"]').xpath('.//*[@class="rg_meta"]/text()').extract()
        for element in elements:
            content = json.loads(element)
            image_url = content.get("ou")
            self.logger.info(content)
            # item['image'] = small_image
            item['image_url'] = image_url
            item['search_engine'] = 'google.com'
            self.logger.info(item)
            yield item
