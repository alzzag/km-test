from django.db import models

	
class Client(models.Model):
	name = models.CharField(max_length=32)
	surname = models.CharField(max_length=32)
	birthday = models.DateField()
	photo = models.FileField(upload_to='photo')
	rating = models.IntegerField(default=0)
	