from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^prediction/$', views.prediction, name='prediction'),
    url(r'^front/$', views.front, name='front'),
    url(r'^rear/$', views.rear, name='rear'),
    url(r'^left/$', views.left, name='left'),
    url(r'^right/$', views.right, name='right'),
    ]

