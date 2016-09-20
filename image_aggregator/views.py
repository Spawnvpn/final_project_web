from django.core.paginator import Paginator
from django.db.models.functions import datetime
from django.shortcuts import render, redirect
from django.views.generic import ListView
from image_aggregator.models import Result, Task
from scrapyd_control import SpiderManage
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
    keywords = request.GET.get('keywords')

    qs = Result.objects.filter(life_expiration__gt=datetime.datetime.now(), task__keywords__icontains=keywords)
    if qs:
        paginator = Paginator(qs, 12)
        page = request.GET.get('page', 1)
        qs = paginator.page(page)
        return render(request, template_name='image_aggregator/image_list.html', context={'images_list': qs})

    log.debug('Client: ' + request.META.get('REMOTE_ADDR') + ' entered: ' + keywords)
    request.session['keywords'] = keywords
    csrftoken = request.COOKIES.get('csrfmiddlewaretoken')

    if request.method == 'GET' and keywords:
        manage = SpiderManage(keywords, csrftoken)
        manage.initialize_spiders()
        manage.run_spiders()
        tasks_ids_list = manage.dump_tasks()
        request.session['tasks_hashes'] = tasks_ids_list.values()
        return redirect('/process/', kwargs=keywords)

    return render(request, template_name='image_aggregator/index.html')


def process_view(request):
    """
    Render the template with the performance of tasks.
    """
    if request.method == 'GET':
        return render(request, template_name='image_aggregator/process.html')


class ImageListView(ListView):
    """
    :returns template with image list if queryset with images exists.
    """
    model = Result
    template_name = 'image_aggregator/image_list.html'
    context_object_name = 'images_list'
    paginate_by = 12

    def get_queryset(self):
        qs = super(ImageListView, self).get_queryset()
        task_hashes = self.request.session.get("tasks_hashes", [])
        return qs.filter(task__job__in=task_hashes, task__is_done=True).order_by('relevance')
