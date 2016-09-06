from django.conf.urls import url
from image_aggregator import views

urlpatterns = [
    url(r'^search/$', view=views.search_view),
    url(r'^process/$', view=views.process_view),
    url(r'^result/page/(?P<page>\d+)/$', view=views.ImageListView.as_view()),
    url(r'^result/(?P<query>\w+)$', view=views.ImageListView.as_view(), name='image_list'),
    url(r'^result/$', view=views.ImageListView.as_view(), name='image_list'),
    url(r'^$', view=views.index),
]
