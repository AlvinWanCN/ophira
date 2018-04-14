#coding:utf-8
from django.shortcuts import render_to_response
from sophiroth.models import *
import hashlib
import modules.get_weather as  get_weather
from django.http import JsonResponse
from sophiroth.forms import *
# Create your views here.




def base(request):
    return render_to_response('base.html',locals())

def main_page(request):
    if request.method == "POST" and request.POST:
        nowTime=time.strftime('%Y-%m-%d %H:%M:%S')
        weatherStatus = get_weather.get_status()
        weatherMax = get_weather.get_max_temperature()
        weatherMin = get_weather.get_min_temperature()
        login = Login(request.POST)
        return render_to_response('main_content.html', locals())
    else:
        login = Login()
        return render_to_response('main.html',locals())

def reqTest(request):
    return render_to_response('reqTest.html',locals())

def ip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return render_to_response('ip.html',locals())


def register(request):
    if request.method == 'POST' and request.POST:
        register = Register(request.POST)
        if register.is_valid(): #判断是否校验是否成功
            data = register.cleaned_data #将校验成功的数据以字典的形式返回
        username = request.POST['username']  #username为我们前端html里面的name的值
        password = request.POST['password']
        email = request.POST['email']
        hash = hashlib.md5()
        hash.update(password)
        password = hash.hexdigest()
        u = User()
        u.username = username
        u.password = password
        u.email = email
        u.save()
    else:
        register = Register()
    return render_to_response("register.html",locals())