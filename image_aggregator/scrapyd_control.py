from image_aggregator.models import Task
from scrapyd_api import ScrapydAPI, constants
from scrapyd_api.compat import iteritems
from raven.contrib.django.raven_compat.models import client


class SpiderManage(object):
    """
    Provides methods for working with ScrapydAPI.
    """
    API_URL = 'http://localhost:6800'
    PROJECT = 'web_bot'

    def __init__(self, keywords, csrftoken):
        self.keywords = keywords
        self.csrftoken = csrftoken
        self.spiders = None
        self.api = None
        self.id_dict = dict()

    def initialize_spiders(self):
        """
        Initializes spiders and returns them to the list :self.spiders
        """
        self.api = ScrapydAPI2(self.API_URL)
        try:
            self.spiders = self.api.list_spiders(self.PROJECT)
        except:
            client.captureException()

    def run_spiders(self):
        """
        Iterates through the list with the spiders, creating a task schedule for scrapy.
        Each new schedule returns hash id of task in :task_id.
        """
        for spider in self.spiders:
            try:
                task_id = self.api.schedule(self.PROJECT, spider, kwargs={'keywords': self.keywords, 'csrftoken': self.csrftoken})
                self.id_dict[spider] = task_id
            except:
                client.captureException()

    def dump_tasks(self):
        """
        Saves the task for each spider in the database and
        :returns self.id_dict where key=spider name, value=hash id of spider.
        """
        for key, value in self.id_dict.items():
            try:
                Task.objects.create(
                    job=value,
                    keywords=self.keywords,
                    is_done=False,
                    spider_name=key,
                )
            except:
                client.captureException()
        return self.id_dict


class ScrapydAPI2(ScrapydAPI):

    def schedule(self, project, spider, settings=None, **kwargs):
        """
        Schedules a spider from a specific project to run. First class, maps
        to Scrapyd's scheduling endpoint.
        """

        url = self._build_url(constants.SCHEDULE_ENDPOINT)
        data = {
            'project': project,
            'spider': spider
        }
        for key, value in kwargs['kwargs'].items():
            data[key] = value
        if settings:
            setting_params = []
            for setting_name, value in iteritems(settings):
                setting_params.append('{0}={1}'.format(setting_name, value))
            data['setting'] = setting_params
        json = self.client.post(url, data=data)
        return json['jobid']
