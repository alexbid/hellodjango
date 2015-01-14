import requests
import sqlite3

from django.shortcuts import render
from django.http import HttpResponse

# from .models import Greeting
from hellodjango.module_one 
portfolioDB = ~\hellodjango\module_one\portfolio.db

print portfolioDB

# request data here
def getLastClose():
	BBG = '^FCHI'
	flag = 'close'
	conn = sqlite3.connect(portfolioDB)
	c = conn.cursor()
	c.execute('SELECT spot FROM (SELECT  MAX(date), spot FROM spots WHERE BBG = ? and flag = ?)', (BBG, flag))

	data = c.fetchone()[0]
	if data == 0:
		conn.close()
		return 'check your data, no spot available'
	else:
        	conn.close()
		return data

# Create your views here.
def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    r = "Salut Alex" + getLastClose()
    #print r.text
    #return HttpResponse('<pre>' + r.text + '</pre>')
    print r
    return HttpResponse('<pre>' + r + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


