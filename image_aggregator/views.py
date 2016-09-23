import hashlib

import redis
from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.shortcuts import render, redirect
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


def search_view(request, **kwargs):
    """
    Takes the desired keywords and creates tasks of spiders.
    """
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    if request.method == 'POST':
        return redirect('search', **{'query': request.POST['q'], 'page': request.POST.get('page', '1')})

    if request.method == "GET":
        page = kwargs.get('page')
        keywords = kwargs.get('query')

    qs = Result.objects.filter(life_expiration__gt=datetime.datetime.now(), task__keywords__icontains=keywords).order_by('relevance')

    if qs:
        paginator = Paginator(qs, 12)
        qs = paginator.page(page)
        return render(request, template_name='image_aggregator/search.html', context={'images_list': qs,
                                                                                      'q': keywords})
    log.debug('Client: ' + request.META.get('REMOTE_ADDR') + ' entered: ' + keywords)

    if request.method == 'GET' and keywords:
        manage = SpiderManage(keywords)
        manage.initialize_spiders()
        manage.run_spiders()
        tasks_id_dict = manage.dump_tasks()
        # hashed_keywords = hashlib.md5(keywords)
        r.set(keywords, json.dumps(tasks_id_dict))
        r.set('quantity_spiders', len(tasks_id_dict.values()))
        response = render(request, template_name='image_aggregator/search.html', context={'q': str(keywords)})
        response['Cache-Control'] = 'no-cache'
        return response

    return render(request, template_name='image_aggregator/index.html')
