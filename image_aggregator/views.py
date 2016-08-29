from django.shortcuts import render
from image_aggregator.models import SearchHistory
# from image_aggregator.tasks import start_google_spider


def index(request):
    return render(request, template_name='image_aggregator/aggregator.html')


def search_view(request):
    # SearchHistory.objects.create(search_phrase=request.GET['phrase'])
    # start_google_spider.apply_async(args=((request.GET.get('phrase')),))
    return render(request, template_name='image_aggregator/aggregator.html')
