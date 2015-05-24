

from django.db import models 

class Signals(models.Model): 
	Date = models.DateField()
	Close = models.FloatField() #(decimal_places=2)
	#mavg_30 = models.FloatField() #(decimal_places=2)
	ewma_10 = models.FloatField() #(decimal_places=2)
	ewma_20 = models.FloatField() #(decimal_places=2)
	ewma_50 = models.FloatField() #(decimal_places=2)
	ewma_100 = models.FloatField() #(decimal_places=2)
	var = models.FloatField() #(decimal_places=2)
	mean = models.FloatField() #(decimal_places=2)
	cv = models.FloatField() #(decimal_places=2)
	BBG = models.CharField(max_length=12)
	lastUpdate = models.DateTimeField()
	
	#libelle = models.CharField(max_length=200) 
	#status =  models.IntegerField() 
		
	def __unicode__(self): 
		return self.BBG
		
	def getLastUpdate(self):
		
		
		
		
		return 2