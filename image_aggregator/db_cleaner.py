from django.db.models.functions import datetime

from models import Result


def cleaner():
    Result.objects.filter(life_expiration__lte=datetime.datetime.today()).delete()
