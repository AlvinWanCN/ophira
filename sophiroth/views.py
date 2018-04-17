#coding:utf-8
from django.shortcuts import render_to_response
from sophiroth.models import *
import hashlib
import sophiroth.modules.get_weather as  get_weather
from django.http import JsonResponse
from sophiroth.forms import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import StreamingHttpResponse

# Create your views here.


def loginValid(fun):
    """
    进行session验证
    目的
        如果不通过login直接访问index,会因为被检测session不存在而去登录
    :param fun:
    :return:
    """
    def inner(request,*args,**kwargs):
        if not request.session.get("name"):
            return HttpResponseRedirect("/login/")
        return fun(request,*args,**kwargs)
    return inner



def hashpassword(password):
    """
    统一进行hash加密
    :param password:
    :return:
    """
    hash = hashlib.md5()
    hash.update(password)
    password = hash.hexdigest()
    return password




def client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip

def auth(Username,Password):
    try:
        filter_u = User.objects.filter(username=Username)[0]
        if filter_u.password == Password:
            return True
        else:
            return False
    except:
        return False



def login(request):
    if request.method == "POST" and request.POST:
        username = request.POST['username']  # username为我们前端html里面的name的值
        password = hashpassword(request.POST['password'])
        if auth(username, password):
            request.session['name'] = username
            #response = index(request)
            return HttpResponseRedirect("/")
        else:
            return render_to_response('login.html', locals())

    else:
        return render_to_response('login.html', locals())



def base(request):
    return render_to_response('base.html',locals())

@loginValid
def index(request):
    ip = client_ip(request)
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    weatherStatus = get_weather.get_status()
    weatherMax = get_weather.get_max_temperature()
    weatherMin = get_weather.get_min_temperature()
    #login = Login(request.POST)
    name = request.session['name']
    return render_to_response('index.html', locals())



def new_account_content(request):
    if request.method == 'POST' and request.POST:
        username = request.POST['username']  #username为我们前端html里面的name的值
        password = request.POST['password']
        application = request.POST['application']
        comment = request.POST['comment']
        u = Account()
        u.username = username
        u.password = password
        u.application = application
        u.comment = comment
        u.save()
    return render_to_response("new_account.html", locals())
def noRightCookie(request):
    if request.method == "POST" and request.POST:
        username = request.POST['username']  # username为我们前端html里面的name的值
        password = hashpassword(request.POST['password'])
        if auth(username, password):

            response = index(request)
            return response
        else:
            return login(request)
    else:
        return login(request)

def check_cookie(request,content):
    if request.COOKIES:
        if request.COOKIES['name'] == 'alvin':
            response = content
            return response
        else:
            return noRightCookie(request)
    else:
        return HttpResponseRedirect('/')
       # return noRightCookie(request)
def check_session(request,content):
    if request.session:
        if request.session['name'] == 'diana':
            response = content
            return response
        else:
            return noRightCookie(request)
    else:
        return HttpResponseRedirect('/')

def main_page(request):
    if request.COOKIES:
        try:
            if request.COOKIES['name'] == 'alvin':
                response = index(request)
                return response
            else:
                return noRightCookie(request)
        except:
            return noRightCookie(request)
    else:
        return noRightCookie(request)

def reqTest(request):
    try:
        cname=request.COOKIES["name"]
        sname=request.session['name']
    except:
        pass
    try:
        sname=request.session['name']
    except:
        pass
    return render_to_response('reqTest.html',locals())


def ip(request):
    ip = client_ip(request)
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


def testcookie(request):

    response = render_to_response('testCookie.html',locals())
    response.set_cookie("name","alvin",3600)

    return response



def testsission(request):
    request.session['name'] = 'diana'
    return render_to_response('testSession.html',locals())

def new_account(request):
    return check_cookie(request,new_account_content(request))

