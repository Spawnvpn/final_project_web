from django.shortcuts import render, redirect
from django.views.generic import ListView
from image_aggregator.models import Result
from scrapyd_control import SpiderManage


def index(request):
    return render(request, template_name='image_aggregator/index.html')


def search_view(request):
    keywords = request.GET.get('keywords')
    if request.method == 'GET' and keywords:
        manage = SpiderManage(keywords)
        manage.initialize_spiders()
        manage.run_spiders()
        tasks_ids_list = manage.dump_tasks()
        keywords = keywords.replace(' ', '+')
        request.session['tasks_hashes'] = tasks_ids_list.values()
        return redirect('/result/')
    return render(request, template_name='image_aggregator/index.html')


class ImageListView(ListView):
    model = Result
    template_name = 'image_aggregator/image_list.html'
    context_object_name = 'images_list'

    def get_queryset(self):
        qs = super(ImageListView, self).get_queryset()
        task_hashes = self.request.session.get("tasks_hashes", [])
        return qs.filter(task__job__in=task_hashes, task__is_done=True)
