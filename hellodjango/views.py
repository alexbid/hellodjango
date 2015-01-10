import requests

from django.shortcuts import render
from django.http import HttpResponse

# from .models import Greeting

# Create your views here.
def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    r = "Salut Alex"
    #print r.text
    #return HttpResponse('<pre>' + r.text + '</pre>')
    print r
    return HttpResponse('<pre>' + r + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})