import scrapy
import json
from scrapy.loader import ItemLoader
from web_bot.items import ImageItem


class InstagramImageSpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        super(InstagramImageSpider, self).__init__(*args, **kwargs)
        self.keywords = kwargs.get('keywords')
        self.csrftoken = kwargs.get('csrftoken')
        self.job = kwargs.get('_job')
        self.logger.info(self.keywords)
        self.logger.info(self.csrftoken)
    name = 'instagram'

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
        item_loader = ItemLoader(item=ImageItem(), response=response)
        image_list = list()
        elements = response.xpath('//p/text()').extract()[0]
        elements = json.loads(elements)['tag']['media']['nodes']
        for element in elements:
            image_list.append(element['thumbnail_src'])
        item_loader.add_value('image_url', image_list)
        item_loader.add_value('job_id', self.job)
        item_loader.add_value('csrftoken', self.csrftoken)
        return item_loader.load_item()
