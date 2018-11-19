from django.conf.urls import url
from . import views	
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.create),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^myaccount/(?P<id>\d+)$', views.myaccount),
    url(r'^update/(?P<id>\d+)$', views.update),
]
