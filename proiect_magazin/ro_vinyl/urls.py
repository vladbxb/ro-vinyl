"""
URL-uri pentru aplicatia web
"""
from django.urls import path
from . import views
# We tie the index request from views.py to the /index endpoint
urlpatterns = [
    path('', views.index, name='index'),
    path('exemplu_simplu/', views.afis_template, name='afis_template'),
]
