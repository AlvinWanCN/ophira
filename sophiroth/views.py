#coding:utf-8
from django.shortcuts import render_to_response
from django.shortcuts import render
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
        if not request.session.get("user_id"):
            return HttpResponseRedirect("/login/")
        return fun(request, *args, **kwargs)

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

def auth_pass(request):
    if request.method == "POST" and request.POST:
        username = request.POST['username']  # username为我们前端html里面的name的值
        password = hashpassword(request.POST['password'])
        if auth(username,password):
            return JsonResponse({'message': 'yes'})
        else:
            return JsonResponse({'message': 'no'})
    else:
        return JsonResponse({'message':'please enter you password'})

def login(request):
    Login = loginForm()
    if request.method == "POST" and request.POST:
        username = request.POST['username']  # username为我们前端html里面的name的值
        password = hashpassword(request.POST['password'])
        Login = loginForm(request.POST)
        if Login.is_valid(): #判断是否校验是否成功
            data = Login.cleaned_data #将校验成功的数据以字典的形式返回
        if auth(username, password):
            request.session['user_id'] = User.objects.filter(username=username)[0].id
            return HttpResponseRedirect("/")
        else:
            return render_to_response('login.html', locals())
    else:
        return render_to_response('login.html', locals())



@loginValid
def index(request):

    weatherStatus = get_weather.get_status()
    weatherMax = get_weather.get_max_temperature()
    weatherMin = get_weather.get_min_temperature()
    role = User.objects.filter(id=request.session['user_id'])[0].role
    ip = client_ip(request)
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    nickname = User.objects.filter(id=request.session['user_id'])[0].nickname
    cpassword='aaaa'
    return render_to_response('index.html', locals())



@loginValid
def new_account(request):
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


def logout(request):
    try:
        del request.session['user_id']
    except:
        pass
    return HttpResponseRedirect("/login")

def reqTest(request):
    try:
        cname=request.COOKIES["idname"]
    except:
        pass
    try:
        id=request.session['id']
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
        u = User()
        u.username = request.POST['username']
        u.password = hashpassword(request.POST['password'])
        u.email = request.POST['email']
        u.nickname = request.POST['nickname']
        u.birthday = request.POST['birthday']
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


def blogroll(request):
    return render_to_response('blogroll.html',locals())

def frame_test(request):
    return render_to_response('frame_test.html',locals())

def iview_test(request):
    return render_to_response('iview_test.html',locals())

@loginValid
def change_password(request):
    nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
    nickname = User.objects.filter(id=request.session['user_id'])[0].nickname
    return render_to_response('change_password.html',locals())

def new_login(request):
    # Login = loginForm()
    # if request.method == "POST" and request.POST:
    #     username = request.POST['username']  # username为我们前端html里面的name的值
    #     password = hashpassword(request.POST['password'])
    #     Login = loginForm(request.POST)
    #     if Login.is_valid(): #判断是否校验是否成功
    #         data = Login.cleaned_data #将校验成功的数据以字典的形式返回
    #     if auth(username, password):
    #         request.session['user_id'] = User.objects.filter(username=username)[0].id
    #         return HttpResponseRedirect("/")
    #     else:
    #         return render_to_response('new_login.html', locals())
    # else:
        return render_to_response('new_login.html', locals())

def jstest(request):
    return render_to_response('jstest.html',locals())
def jstest1(request):
    return render_to_response('js_test1.html',locals())

def favicon(request):
    return render_to_response('/static/img/favicon.ico')

def jqajax_test(request):
    return render_to_response('jqajax.html',locals())

def jquery_test(request):
    return render_to_response('jquery_test.html',locals())