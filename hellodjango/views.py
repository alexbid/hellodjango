import requests
import sqlite3
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response 
import os
import psycopg2
import urlparse
from hellodjango.models import Signals 
#
#def getLastClose():
#	BBG = '^FCHI'
#	flag = 'close'
#
#	try: 
#		urlparse.uses_netloc.append("postgres")
#		if not os.environ.has_key('DATABASE_URL'):
#			os.environ['DATABASE_URL'] = 'postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb?sslca=config/ca/rds-ssl-ca-cert.pem&sslmode=require&encrypt=true'
#			
#		url = urlparse.urlparse(os.environ["DATABASE_URL"])
#		conn = psycopg2.connect(
#			database='marketdb',
#			user='awsuser',
#			password='Newyork2012',
#			host='awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com',
#			port=5432
#		)
#		c = conn.cursor()
#		c.execute("""SELECT "Close" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG = %s) AND BBG = %s)""", (BBG, BBG))
#		
#		data = c.fetchone()[0]
#		if data == 0:
#			conn.close()
#			return 'check your data, no spot available'
#		else: 
#			conn.close()
#			return data
#	except ValueError: 
#		return "Ops!! Connection to DB failed!!" 

def index(request):
	signals = Signals.objects.distinct('BBG').order_by('BBG')
	return render_to_response('home.html', {'signals': signals})

from datetime import datetime
#from django.shortcuts import render_to_response

def my_date_view(request, ws_date_as_datetime):
    the_date = datetime.strftime(ws_date, "%Y-%m-%d %H:%M:%S+0000")
    return render_to_response('home.html', {'date':the_date})

"""def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})
"""

