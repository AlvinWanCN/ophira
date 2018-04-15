#coding:utf-8
from django.db import models
import time
# Create your models here.



class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

class Account(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    application = models.CharField(max_length=50)
    comment = models.CharField(max_length=254)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

