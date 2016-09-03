# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class ImageItem(Item):
    csrftoken = Field()
    task = Field()
    image_url = Field()
    small_image_url = Field()
    search_engine = Field()
    origin_url = Field()
    job_id = Field()

