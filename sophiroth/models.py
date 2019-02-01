#coding:utf-8
from django.db import models
import time
# Create your models here.



class User(models.Model):
    id = models.CharField(max_length=40,null=False,primary_key=True)
    username = models.CharField(max_length=32,null=False)
    nickname = models.CharField(max_length=32,null=False)
    password = models.CharField(max_length=50,null=False)
    email = models.CharField(max_length=50,null=True)
    birthday = models.DateField(null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    role = models.IntegerField(default=0)

class Account(models.Model):
    id = models.CharField(max_length=40, null=False,primary_key=True)
    username = models.CharField(max_length=50,null=False)
    password = models.CharField(max_length=50,null=False)
    application = models.CharField(max_length=50,null=False)
    comment = models.CharField(max_length=254)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    uid = models.CharField(max_length=40,null=False)

class Apps(models.Model):
    id = models.CharField(max_length=40, null=False,primary_key=True)
    path = models.CharField(max_length=32,null=False)
    name = models.CharField(max_length=32,null=False)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=254)
    uid = models.CharField(max_length=40,null=False)

