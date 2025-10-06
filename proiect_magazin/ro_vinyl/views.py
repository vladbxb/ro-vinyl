from django.http import HttpResponse

# Create your views here.
def index(request):
    """Ruta principala pentru aplicatia web."""
    return HttpResponse('Primul raspuns')
