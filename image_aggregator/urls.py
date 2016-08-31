from django.conf.urls import url
from image_aggregator import views

urlpatterns = [
    url(r'^search/', view=views.search_view),
    url(r'^result/', view=views.ImageListView.as_view()),
    url(r'^', view=views.index),
]
