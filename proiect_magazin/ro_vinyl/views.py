from django.http import HttpResponse
from django.shortcuts import render

def afis_template(request):
    return render(request,"ro_vinyl/simplu.html",
        {
            "param":"valoare",
        }
    )


# Create your views here.
def index(request):
    """Ruta principala pentru aplicatia web."""
    return HttpResponse('Primul raspuns')

