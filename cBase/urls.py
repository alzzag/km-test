from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.client_list, name='client_list'),
    url(r'^export$', views.export_excel, name='export_excel'),
    url(r'^photos$', views.photos, name='photos')
]