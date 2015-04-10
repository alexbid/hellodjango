from code_python import Stock
import datetime
import numpy as np

class Share(Stock):
	
	def toto(self):
		return "toto"
		
	#def load(self, startD, endD, flag):
		
		
if __name__=='__main__':

	startdt = datetime.date(2015, 01, 01)
	enddt = datetime.date(2015, 4, 10)

	x = Share("^FCHI")
	#a = np.array([ 0, 0.5, 1.0, 1.5, 2.0])
	#print a.sum()
	#print a.std()
	x.load_pandas(startdt, enddt, 'close')
	
	res = x.spots#[:: 100] # every 100th result

	yhoo = res[['date', 'spot', 'mavg_30', 'ewma_10', 'ewma_20', 'ewma_50', 'ewma_100']]
	#print yhoo
	
	import matplotlib.pyplot as plt 
	plt.title('Graph: ' + x.getMnemo() )
	yhoo['spot'].plot(label='CAC40')
	yhoo['mavg_30'].plot(label='mavg_30')
	yhoo['ewma_10'].plot(label='ewma_10')
	yhoo['ewma_20'].plot(label='ewma_20')
	yhoo['ewma_50'].plot(label='ewma_50')
	yhoo['ewma_100'].plot(label='ewma_100')
	plt.xlabel(yhoo['date'])
#	yhoo.plot.plot(style='r', lw = 2.)
#	yhoo['spot'].plot(figsize =( 8, 5))



	#plt.legend()
	plt.show()