from django.http import HttpResponse
from django.shortcuts import render

def exemplu_afis_template(request):
    return render(request,"ro_vinyl/simplu.html",
        {
            "param":"valoare",
        }
    )

# Create your views here.
def index(request):
    """Ruta principala pentru aplicatia web."""
    return render(request,"ro_vinyl/pagina_principala.html",
        {
            "param":"valoare",
        }
    )

def despre(request):
    """Ruta pentru pagina despre"""
    return render(request, "ro_vinyl/despre.html")

def catalog(request):
    """Ruta pentru pagina catalog"""
    # pagina este in lucru
    return render(request, "ro_vinyl/in_lucru.html")

def contact(request):
    """Ruta pentru pagina contact"""
    # pagina este in lucru
    return render(request, "ro_vinyl/in_lucru.html")