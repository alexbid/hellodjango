import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())
    
def update()
	import sys
	import datetime
	from module_one.code_python import Portfolio
	from module_one.code_python import vTradingDates
	from module_one.code_python import doRequestData

	dt = datetime.date(1990, 03, 01)
	end = datetime.date(2015, 12, 30)

	doRequestData('^FCHI', dt, end)
	