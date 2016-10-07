from __future__ import absolute_import
import os
from celery.task import periodic_task
from datetime import timedelta

from django.db.models.functions import datetime
from image_aggregator.models import Result
from celery import Celery


@periodic_task(run_every=timedelta(seconds=86400))
def clear_old():
    Result.objects.filter(life_expiration__lte=datetime.datetime.today()).delete()
