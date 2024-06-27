from django.db import models

# Create your models here.
class UsrCredentials(models.Model):
    usrname = models.CharField(max_length=100)
    llat = models.CharField(max_length=500) #long lived access token
    pgat = models.CharField(max_length=500) #fb page access token
    iguserid = models.IntegerField()
    fbpageid = models.IntegerField()
    appid = models.IntegerField()
    appsecret = models.CharField(max_length=200)