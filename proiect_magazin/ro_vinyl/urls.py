"""
URL-uri pentru aplicatia web
"""
from django.urls import path, re_path
from . import rute
from . import views
# We tie the index request from views.py to the /index endpoint
urlpatterns = [
    path('', views.index, name='index'),
    path('/', views.index, name='index'),
    path('despre', views.despre, name='despre'),
    path('catalog', views.catalog, name='catalog'),
    path('contact', views.contact, name='contact'),
    path('info', rute.info, name="info"),
    path('info/', rute.info, name="info"),
    path('info/data', rute.static_data, name="static_data"),
    path('info/data/', rute.static_data, name="static_data"),
    re_path(r'^info/data/(zi|timp)$', rute.afis_data, name="afis_data"),
    re_path(r'^info/data/(zi|timp)/$', rute.afis_data, name="afis_data"),
    path('log', rute.log, name="static_log"),
    path('log/', rute.log, name="static_log"),
    path('exemplu_simplu', views.exemplu_afis_template, name='afis_template'),
    path('exemplu_simplu/', views.exemplu_afis_template, name='afis_template'),
]
