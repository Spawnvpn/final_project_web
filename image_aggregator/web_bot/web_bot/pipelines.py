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
        self.conn.execute('insert into image_aggregator_searchhistory(image_url, small_image, search_engine, search_state) values(?, ?, ?, ?)',
                          (item.get('image_url'), item.get('image'), item.get('search_engine'), '1'))
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
