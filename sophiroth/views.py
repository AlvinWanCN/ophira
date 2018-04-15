#coding:utf-8
from django.shortcuts import render_to_response
from sophiroth.models import *
import hashlib
import sophiroth.modules.get_weather as  get_weather
from django.http import JsonResponse
from sophiroth.forms import *
# Create your views here.



def auth(Username,Password):
    try:
        filter_u = User.objects.filter(username=Username)[0]
        if filter_u.password == Password:
            return True
        else:
            return False
    except:
        return False

def base(request):
    return render_to_response('base.html',locals())

def main_content(request):
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    weatherStatus = get_weather.get_status()
    weatherMax = get_weather.get_max_temperature()
    weatherMin = get_weather.get_min_temperature()
    login = Login(request.POST)
    response = render_to_response('main_content.html', locals())
    response.set_cookie("name", "alvin", 3600)
    return response

def noRightCookie(request):
    if request.method == "POST" and request.POST:
        username = request.POST['username']  # username为我们前端html里面的name的值
        password = request.POST['password']
        hash = hashlib.md5()
        hash.update(password)
        password = hash.hexdigest()
        if auth(username, password):
            response = main_content(request)
            return response
        else:
            response = render_to_response('main.html', locals())
            return response
    else:
        login = Login()
        response = render_to_response('main.html', locals())
        return response
def main_page(request):
    if request.COOKIES:
        if request.COOKIES['name'] == 'alvin':
            response = response = main_content(request)
            return response
        else:
            return noRightCookie(request)
    else:
        return noRightCookie(request)

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


def testcokie(request):
    cname=request.COOKIES["name"]
    response = render_to_response('testCookie.html',locals())
    response.set_cookie("name","alvin",3600)
    return response
