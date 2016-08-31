from django.shortcuts import render
from image_aggregator.models import Task
from scrapyd_api import ScrapydAPI


def index(request):
    return render(request, template_name='image_aggregator/aggregator.html')


def search_view(request):
    API_URL = 'http://localhost:6800'
    keywords = request.GET.get('keywords')
    if request.method == 'GET'and keywords:

        google = ScrapydAPI(API_URL)
        yandex = ScrapydAPI(API_URL)
        instagram = ScrapydAPI(API_URL)

        google_job_id = google.schedule('web_bot', 'yandeximagespider', kwargs=keywords)
        yandex_job_id = yandex.schedule('web_bot', 'googleimagespider', kwargs=keywords)
        instagram_job_id = instagram.schedule('web_bot', 'instagramimagespider', kwargs=keywords)

        Task.objects.create(
            job=google_job_id,
            keywords=keywords,
            is_done=False,
        )
        Task.objects.create(
            job=yandex_job_id,
            keywords=keywords,
            is_done=False,
        )
        Task.objects.create(
            job=instagram_job_id,
            keywords=keywords,
            is_done=False,
        )
        print google_job_id, yandex_job_id, instagram_job_id

    return render(request, template_name='image_aggregator/aggregator.html')
