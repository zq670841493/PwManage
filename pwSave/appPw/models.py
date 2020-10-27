from django.db import models


#密码存储列信息
class pwInfo(models.Model):
    webname =models.CharField(max_length=100)
    weblink = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    other = models.CharField(max_length=100)
    userID = models.CharField(max_length=32)


#密码存储列信息日志
class pwInfoLog(models.Model):
	webname =models.CharField(max_length=100)
	time = models.CharField(max_length=100)
	changelog=models.CharField(max_length=100)
	userID = models.CharField(max_length=32)

