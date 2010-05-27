# Create your views here.
from django.template import loader, Context
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello World")
    
    