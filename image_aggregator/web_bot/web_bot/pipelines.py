# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import django
# from image_aggregator.models import SearchHistory


class WebBotPipeline:

    # def __init__(self):
    #     django.setup()

    def process_item(self, item, spider):
        image_url = item.get("image_url", None)
        if image_url:
            SearchHistory.objects.create(image_url=image_url)
        return item
