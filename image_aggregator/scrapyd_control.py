from scrapyd_api import ScrapydAPI


class SpiderManage(object):
    def __init__(self, keywords):
        self.API_URL = 'http://localhost:6800'
        self.keywords = keywords

    def initialize_spiders(self):
        google = ScrapydAPI(self.API_URL)
        yandex = ScrapydAPI(self.API_URL)
        instagram = ScrapydAPI(self.API_URL)

    def run_spiders(self):
        google_job_id = google.schedule('web_bot', 'yandeximagespider', kwargs=self.keywords)
        yandex_job_id = yandex.schedule('web_bot', 'googleimagespider', kwargs=self.keywords)
        instagram_job_id = instagram.schedule('web_bot', 'instagramimagespider', kwargs=self.keywords)
