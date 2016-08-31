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
        # try:
        job_id = item.get('job_id')
        task_id = self.conn.execute('SELECT id FROM image_aggregator_task WHERE job="%s"' % job_id)
        task_id = task_id.fetchone()
        self.conn.execute('insert into image_aggregator_result(image_url, small_image_url, search_engine, origin_url, task_id) values(?, ?, ?, ?, ?)',
                          (item.get('image_url'), item.get('image'), item.get('search_engine'), item.get('origin'), task_id[0]))
        self.conn.execute('UPDATE image_aggregator_task SET is_done=1 WHERE job="%s"' % job_id)
        # except:
        #     print('Failed to insert item: ' + item['image_url'])
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

# class WebBotPipeline:
#
#     def process_item(self, item, spider):
#         image_url = item.get("image_url", None)
#         if image_url:
#             SearchHistory.objects.create(image_url=image_url)
#         return item
