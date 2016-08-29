import json
import scrapy


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
            self.req = "cat"
        start_urls = ['https://yandex.ua/images/search?text=' + self.req]
        return start_urls

    def parse(self, response):
        item = dict()
        # inspect_response(response, self)
        elements = response.xpath('//div[contains(@class, "serp-list_type_search")]')
        elements.extract()
        for element in elements:
            small_image = 'http:' + element.xpath('.//div/a/img/@src').extract()[0]
            content = element.xpath('.//div/@data-bem').extract()[0]
            content = json.loads(content)
            self.logger.info(content)
            content = content.get("serp-item")
            content = content.get("preview")
            content = content[0].get("url")
            image_url = content
            self.logger.info(content)
            item['image'] = small_image
            item['image_url'] = image_url
            item['search_engine'] = 'yandex.ua'
            yield item
