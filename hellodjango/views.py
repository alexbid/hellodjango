import requests
import sqlite3

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response 

# from .models import Greeting
# from hellodjango.module_one 

import os
#output = os.path.realpath(os.path.dirname(__file__))
#SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
#SITE_ROOT = SITE_ROOT[:-12]
#if not output: portfolioDB  = 'portfolio.db'
#else:
#        portfolioDB = output + '/module_one/portfolio.db'
#        output += "/"
#portfolioDB = "/module_one/portfolio.db"
#DATABASE_NAME = os.path.join(SITE_ROOT, 'module_one') + '/portfolio.db'

import psycopg2
import urlparse


# request data here
def getLastClose():
	BBG = '^FCHI'
	flag = 'close'

	try: 
		urlparse.uses_netloc.append("postgres")
		if not os.environ.has_key('DATABASE_URL'):
#			os.environ['DATABASE_URL'] = 'postgres://wcmikblybrgqbz:ZycOXg48gWJlRGR3MVFA9qGxvB@ec2-23-23-210-37.compute-1.amazonaws.com:5432/d3ibjjmjb9fqrm'
#			os.environ['DATABASE_URL'] = 'postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb'
			os.environ['DATABASE_URL'] = 'postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb?sslca=config/ca/rds-ssl-ca-cert.pem&sslmode=require&encrypt=true'
			
		url = urlparse.urlparse(os.environ["DATABASE_URL"])
		#return 'icici c est Paris'
		#try : 
			#conn = sqlite3.connect(DATABASE_NAME)
		conn = psycopg2.connect(
			database='marketdb',
#			database=url.path[1:],
			#user='wcmikblybrgqbz',
			user='awsuser',
			#user=url.username,
			#password=url.password,
			password='Newyork2012',
			host='awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com',
#			host=url.hostname,
#			port=url.port
			port=5432
		)
		#except: return "failed to connect to DB....."
		c = conn.cursor()
		#c.execute('SELECT spot FROM (SELECT  MAX(date), spot FROM spots WHERE BBG = %s and flag = %s) AS FOO', (BBG, flag))
		#c.execute("SELECT spot FROM spots WHERE (date=(SELECT MAX(date) FROM spots WHERE BBG = %s AND flag = %s) AND BBG = %s AND flag = %s)", (BBG, flag, BBG, flag))
		c.execute("""SELECT "Close" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG = %s) AND BBG = %s)""", (BBG, BBG))
		

		data = c.fetchone()[0]
		if data == 0:
			conn.close()
			return 'check your data, no spot available'
		else: 
			conn.close()
			return data
	except ValueError: 
		return "Ops!! Connection to DB failed!!" 

# Create your views here.
#def home(request):
#	return HttpResponse("Hello, world.")

from hellodjango.models import Signals 

def index(request):
	"""
	from rq import Queue
	from worker import conn
	q = Queue(connection=conn)
	from utils import count_words_at_url
	from utils import update
	result = q.enqueue(update)
	r = str(getLastClose())
	return HttpResponse('<pre>' + r + '</pre>')
	"""
	signals = Signals.objects.all() 
	return render_to_response('home.html', {'signals': signals})
	#return render_to_response('home.html')
	
	
def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})


