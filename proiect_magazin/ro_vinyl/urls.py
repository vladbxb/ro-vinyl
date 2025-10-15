"""
URL-uri pentru aplicatia web
"""
from django.urls import path, re_path
from . import rute
from . import views
# We tie the index request from views.py to the /index endpoint
urlpatterns = [
    path('', rute.index, name='index'),
    path('info/', rute.info, name="info"),
    path('info/data/', rute.static_data, name="static_data"),
    re_path(r'^info/data/(zi|timp)$', rute.afis_data, name="afis_data"),
    path('log/', rute.log, name="static_log"),
    path('exemplu_simplu/', views.afis_template, name='afis_template'),
]
