from django.conf.urls import url
from image_aggregator import views

urlpatterns = [
    url(r'^search/$', view=views.search_view),
    # url(r'^search/(?P<query>\w+)$', view=views.search_view),
    url(r'^search/(?P<query>\w+)/(?P<page>\d+)/$', view=views.search_view),
    url(r'^process/$', view=views.process_view),
    url(r'^$', view=views.index),
]
