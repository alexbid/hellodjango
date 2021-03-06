import requests
import sqlite3

from django.shortcuts import render
from django.http import HttpResponse

import os
output = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SITE_ROOT = SITE_ROOT[:-12]

DATABASE_NAME = os.path.join(SITE_ROOT, 'module_one') + '/portfolio.db'

def getLastClose():
	BBG = '^FCHI'
	flag = 'close'

	try: 
		try : conn = sqlite3.connect(DATABASE_NAME)
		except: return "failed to connect to DB: " + DATABASE_NAME + "  pwd: " + output + "  SITE_ROOT: " + SITE_ROOT 
		c = conn.cursor()
		c.execute('SELECT spot FROM (SELECT  MAX(date), spot FROM spots WHERE BBG = ? and flag = ?)', (BBG, flag))
		data = c.fetchone()[0]
		if data == 0:
			conn.close()
			return 'check your data, no spot available'
		else: 
			conn.close()
			return data
	except ValueError: return "Ops!! Connection to DB failed!!"

# Create your views here.
def index(request):
	from rq import Queue
	from worker import conn
	q = Queue(connection=conn)
	
	# And enqueue the function call
	from utils import count_words_at_url
	from utils import update
	result = q.enqueue(update)

	r = str(getLastClose())
	return HttpResponse('<pre>' + r + '</pre>')
	
def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})


