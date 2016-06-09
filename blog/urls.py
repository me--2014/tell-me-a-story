from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    #ex /blog/1
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^filter/$', views.filter, name='filter'),
    url(r'^(?P<tag_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^(?P<tag_id>[0-9]+)/getTaggedStories/$', views.taggedStories, name='taggedStories'),
    url(r'^getMostRecent/$', views.getMostRecent, name='getMostRecent'),
    url(r'^getTags/$', views.getTags, name='getTags'),
    url(r'^toggleFav/$', views.toggleFav, name='toggleFav')
]