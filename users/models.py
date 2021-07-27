from django.db import models

# Create your models here.
class User(models.Model):
	Name = models.CharField(max_length=120)
	username=models.CharField(max_length=120)
	email=models.EmailField(max_length=254)
	password=models.CharField(max_length=120)
	mobile=models.DecimalField(decimal_places=2,max_digits=1000)

class SetCookie123(models.Model):
	username = models.CharField(max_length=120)
	cookie_id_allocated = models.CharField(max_length=120,blank=True,null=True)