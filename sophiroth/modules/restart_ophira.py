#!/usr/bin/python
#coding:utf-8
import subprocess

subprocess.call("kill -9 `ps -eo pid,cmd|grep /usr/bin/python|grep runserver|grep 8003|awk '{print $1}'`", shell=True)
subprocess.call('nohup python manage.py runserver 0.0.0.0:8003 &>/tmp/8003.log &', shell=True)