from image_aggregator.models import Task
from scrapyd_api import ScrapydAPI
from django.contrib.sessions.backends.db import SessionStore


class SpiderManage(object):
    API_URL = 'http://localhost:6800'
    PROJECT = 'web_bot'

    def __init__(self, keywords):
        self.keywords = keywords
        self.spiders = None
        self.api = None
        self.id_dict = dict()

    def initialize_spiders(self):
        self.api = ScrapydAPI(self.API_URL)
        self.spiders = self.api.list_spiders(self.PROJECT)

    def run_spiders(self):
        for spider in self.spiders:
            task_id = self.api.schedule(self.PROJECT, spider, kwargs=self.keywords)
            self.id_dict[spider] = task_id

    def dump_tasks(self):
        for key, value in self.id_dict.items():
            Task.objects.create(
                job=value,
                keywords=self.keywords,
                is_done=False,
                spider_name=key,
            )
        return self.id_dict
