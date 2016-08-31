from django.db import models


class Task(models.Model):

    job = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    is_done = models.IntegerField(default=False)


class Result(models.Model):

    task = models.ForeignKey(Task)
    image_url = models.CharField(max_length=2000, blank=True, null=True)
    small_image_url = models.CharField(max_length=2000, blank=True, null=True)
    search_engine = models.CharField(max_length=255, blank=True, null=True)
    origin_url = models.CharField(max_length=200, blank=True, null=True)
