# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class WebBotPipeline:
    filename = '/home/bogdan/PycharmProjects/final_project_web/db.sqlite3'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        job_id = item.get('job_id')
        task_id = self.conn.execute('SELECT id FROM image_aggregator_task WHERE job="%s"' % job_id[0])
        task_id = task_id.fetchone()
        query_string = 'insert into image_aggregator_result(image_url, small_image_url, search_engine, origin_url, task_id) values '
        for image in zip(item['image_url']):
            query_string += '("%s", "%s", "%s", "%s", "%s"),' % (image[0], item.get('small_images'), spider.name, item.get('origin'), task_id[0])
        query = query_string[:-1]
        self.conn.execute(query)
        self.conn.execute('UPDATE image_aggregator_task SET is_done=1 WHERE job="%s"' % job_id[0])
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
