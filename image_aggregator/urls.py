from django.conf.urls import url
from image_aggregator import views

urlpatterns = [
    url(r'^search/(?P<query>.*)/(?P<page>\d+)$', view=views.search_view, name='search'),
    url(r'^search/$', view=views.search_view, name='search'),
    url(r'^$', view=views.index),
]
