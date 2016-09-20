import json
import sqlite3
from settings import SENTRY_DSN
import redis
from os import path
from raven import Client
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class WebBotPipeline:
    filename = '/home/bogdan/PycharmProjects/final_project_web/db.sqlite3'

    def __init__(self):
        self.conn = None
        self.buff_item = None
        self.spider_name = None
        self.client = Client(SENTRY_DSN)
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def get_expiration(self):
        date = sqlite3.datetime.datetime.now()
        day = sqlite3.datetime.datetime.now().day + 1
        expiration_date = date.replace(day=day)
        return expiration_date

    def process_item(self, item, spider):
        self.buff_item = item
        self.spider_name = spider.name
        job_id = item.get('job_id')
        task_id = self.conn.execute('SELECT id FROM image_aggregator_task WHERE job="%s"' % job_id[0])
        task_id = task_id.fetchone()
        query_string = 'INSERT INTO image_aggregator_result(image_url, small_image_url, search_engine, origin_url, task_id, relevance, life_expiration) VALUES '
        relevance = 1

        try:
            for big_image, small_image, origin in zip(item['image_url'], item['small_image_url'], item['origin_url']):
                query_string += '("%s", "%s", "%s", "%s", "%s", "%s", "%s"),' % (big_image, small_image, spider.name, origin, task_id[0], relevance, self.get_expiration())
                relevance += 1
        except:
            self.client.captureException()

        query = query_string[:-1]
        self.conn.execute(query)
        self.conn.execute('UPDATE image_aggregator_task SET is_done=1 WHERE job="%s"' % job_id[0])
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        # r.set('%s' % identifier_string, '%s' % self.spider_name)
        # r.expire('%s' % identifier_string, 30)
        r.publish('task_state', '%s' % json.dumps(job_id))

        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
