import json
import scrapy
from scrapy.shell import inspect_response
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings


class GoogleImageSpider(scrapy.Spider):

    def __init__(self, req=None, **kwargs):
        super(GoogleImageSpider, self).__init__(**kwargs)
        self.req = req
    name = 'googleimagespider'
    # req = 'cats'

    def start_requests(self):
        links = self.get_links()
        self.logger.info("LINKS: {}".format(", ".join(links)))
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        if not self.req:
            self.req = "cat"
        start_urls = ['https://www.google.com.ua/search?q=' + self.req + '&source=lnms&tbm=isch']
        return start_urls

    def parse(self, response):
        item = dict()
        # inspect_response(response, self)
        # elements = response.xpath('//*[@id="rg_s"]') # for js
        elements = response.xpath('//*[@id="ires"]/table[@class="images_table"]')
        elements.extract()
        for r in range(1, 6):
            for d in range(1, 5):
                for pic in response.xpath('//*[@id="ires"]/table/tr[' + str(r) + ']/td[' + str(d) + ']'):
                    small_image = pic.xpath('.//a/img/@src').extract()[0]
                    content = pic.xpath('.//a/@href').extract()[0][7:]
                    superflous = content.find('&')
                    content = content[:superflous]
                    self.logger.info(pic)
                    item['image'] = small_image
                    item['image_url'] = content
                    item['search_engine'] = 'google.com'
                    yield item

        # """For js page"""
        # for element in elements:
        #     self.logger.info(element)
        #     content = elements.xpath('./td/a/@href')
            # content = element.xpath('.//*[contains(@class, "rg_di")]/div[@class="rg_meta"]/text()').extract()[0]
            # content = json.loads(content)
            # image_url = content.get("ou")
            # self.logger.info(content)
            # for item
            # item['image_url'] = image_url
            # item['search_engine'] = 'Google'
            # yield {
            #     item
            # }

#
# class GoogleCrawlerScript:
#
#     def __init__(self):
#         self.crawler = CrawlerProcess(Settings())
#         # self.phrase = phrase
#
#     def _crawl(self, phrase):
#         self.crawler.crawl(GoogleImageSpider(phrase))
#         self.crawler.start()
#         self.crawler.stop()
#
#     def crawl(self, phrase):
#         p = Process(target=self._crawl, args=[phrase])
#         p.start()
#         p.join()
#
#
# def google_crawl(phrase):
#     crawler = GoogleCrawlerScript()
#     crawler.crawl(phrase)
