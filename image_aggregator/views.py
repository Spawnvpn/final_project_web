import redis
from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.shortcuts import render
from image_aggregator.models import Result, Task
from scrapyd_control import SpiderManage
import json
import uuid
import logging


log = logging.getLogger(__name__)


def index(request):
    """
    :returns template with main page.
    """
    log.info('Client: ' + request.META.get('REMOTE_ADDR') + ' get index')
    qs = Task.objects.all().order_by('-id')[:30]
    return render(request, template_name='image_aggregator/index.html', context={'context': qs})


def search_view(request):
    """
    Takes the desired keywords and creates tasks of spiders.
    """
    keywords = request.GET.get('q')
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    qs = Result.objects.filter(life_expiration__gt=datetime.datetime.now(), task__keywords__icontains=keywords).order_by('relevance')
    # request.COOKIES['q'] = keywords
    # request.session['q'] = keywords
    if qs:
        paginator = Paginator(qs, 12)
        page = request.GET.get('page', 1)
        qs = paginator.page(page)
        return render(request, template_name='image_aggregator/search.html', context={'images_list': qs})
    log.debug('Client: ' + request.META.get('REMOTE_ADDR') + ' entered: ' + keywords)

    if request.method == 'GET' and keywords:
        manage = SpiderManage(keywords)
        manage.initialize_spiders()
        manage.run_spiders()
        tasks_id_dict = manage.dump_tasks()
        tasks_ids = uuid.uuid1()
        r.set(tasks_ids, json.dumps(tasks_id_dict))
        return render(request, template_name='image_aggregator/search.html', context={'q': str(keywords)})

    return render(request, template_name='image_aggregator/index.html')


def process_view(request):
    """
    Render the template with the performance of tasks.
    """
    if request.method == 'GET':
        return render(request, template_name='image_aggregator/search.html')
