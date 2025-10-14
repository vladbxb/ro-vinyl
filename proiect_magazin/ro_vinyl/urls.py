"""
URL-uri pentru aplicatia web
"""
from django.urls import path, re_path
from . import acces
from . import views
# We tie the index request from views.py to the /index endpoint
urlpatterns = [
    path('', acces.index, name='index'),
    path('info/', acces.info, name="info"),
    path('info/data/', acces.static_data, name="static_data"),
    re_path(r'^info/data/(zi|timp)$', acces.afis_data, name="afis_data"),
    path('log/', acces.log, name="static_log"),
    path('exemplu_simplu/', views.afis_template, name='afis_template'),
]
