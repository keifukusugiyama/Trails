from django.conf.urls import url
from . import views	
urlpatterns = [
    url(r'^$', views.trails_main),
    url(r'^create_trail$', views.create_trail),
    url(r'^(?P<id>\d+)$', views.view_trail),
    url(r'^(?P<id>\d+)/delete_trail$', views.delete_trail),
    url(r'^(?P<id>\d+)/edit_trail$', views.edit_trail),
    url(r'^(?P<id>\d+)/update_trail$', views.update_trail),
]
