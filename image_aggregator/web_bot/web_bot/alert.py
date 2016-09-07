from scrapy import signals
from settings import SENTRY_DSN
from raven import Client


class FailLogger(object):
    client = Client(SENTRY_DSN)

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()

        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_error(self, failure, response, spider):
        try:
            failure.raiseException()
        except:
            self.client.get_ident(self.client.captureException())
