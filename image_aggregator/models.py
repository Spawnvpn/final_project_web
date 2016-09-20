from django.db import models


class Task(models.Model):

    job = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    is_done = models.IntegerField(default=False)
    spider_name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)


class Result(models.Model):

    task = models.ForeignKey(Task, related_name='task')
    image_url = models.CharField(max_length=2000, blank=True, null=True)
    small_image_url = models.CharField(max_length=2000, blank=True, null=True)
    search_engine = models.CharField(max_length=255, blank=True, null=True)
    origin_url = models.CharField(max_length=200, blank=True, null=True)
    relevance = models.PositiveIntegerField(blank=True, null=True)
    life_expiration = models.DateTimeField(null=True)
