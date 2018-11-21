from django.conf.urls import url
from . import views	
urlpatterns = [
    url(r'^user/(?P<id>\d+)$', views.user_report),
    url(r'^(?P<id>\d+)/new_report$', views.new_report),
    url(r'^create_report$', views.create_report),
    url(r'^delete_report$', views.delete_report),
    url(r'^(?P<id>\d+)/edit_report$', views.edit_report),
    url(r'^(?P<id>\d+)/update_report$', views.update_report),
]
