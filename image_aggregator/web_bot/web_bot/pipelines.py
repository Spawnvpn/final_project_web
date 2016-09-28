import json
import psycopg2
from settings import SENTRY_DSN
import redis
from raven import Client
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import settings
from datetime import datetime


class WebBotPipeline:

    def __init__(self):
        self.conn_string = settings.DB_CONN
        self.conn = None
        self.cursor = None
        self.buff_item = None
        self.spider_name = None
        self.client = Client(SENTRY_DSN)
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def get_expiration(self):
        date = datetime.now()
        day = datetime.now().day + 1
        expiration_date = date.replace(day=day)
        return expiration_date

    def process_item(self, item, spider):
        r = redis.StrictRedis().from_url(settings.REDIS_CON)
        self.buff_item = item
        self.spider_name = spider.name
        job_id = item.get('job_id')
        self.cursor.execute("SELECT id FROM image_aggregator_task WHERE job='%s'" % job_id[0])
        task_id = self.cursor.fetchone()
        query_string = "INSERT INTO image_aggregator_result(image_url, small_image_url, search_engine, origin_url, task_id, relevance, life_expiration) VALUES "
        relevance = 1

        try:
            for big_image, small_image, origin in zip(item['image_url'], item['small_image_url'], item['origin_url']):
                query_string += "('%s', '%s', '%s', '%s', '%s', '%s', '%s')," % (big_image, small_image, spider.name, origin, task_id[0], relevance, self.get_expiration())
                relevance += 1
        except:
            self.client.captureException()
            r.publish('task_state', 'error')

        query = query_string[:-1]
        try:
            self.cursor.execute(query + ';')
            self.cursor.execute("UPDATE image_aggregator_task SET is_done=1 WHERE job='%s'" % job_id[0])
        except:
            self.client.captureException()
            r.publish('task_state', 'error')
        r.publish('task_state', '%s' % json.dumps(job_id))

        return item

    def initialize(self):
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def finalize(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        self.conn = None
        self.cursor = None
