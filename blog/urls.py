from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^getStories/$', views.getStories, name='getStories'),
    url(r'^getMostRecent/$', views.getMostRecent, name='getMostRecent'),
    url(r'^getTags/$', views.getTags, name='getTags'),
    url(r'^toggleFav/$', views.toggleFav, name='toggleFav')
]