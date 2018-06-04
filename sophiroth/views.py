#coding:utf-8
from django.shortcuts import render_to_response
from django.shortcuts import render
from sophiroth.models import *
import hashlib,subprocess,os
import sophiroth.modules.get_weather as get_weather
from django.http import JsonResponse
from sophiroth.forms import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import StreamingHttpResponse
import uuid
from sophiroth.modules.sysinfo_api import *
from sophiroth.modules.pages import *
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
            request.session['user_id'] = User.objects.filter(username=username)[0].id
            session_key=request.session.session_key
            # nickname=User.objects.filter(username=username)[0].nickname
            nickname = User.objects.filter(id=request.session['user_id'])[0].nickname
            id=request.session['user_id']
            print(session_key)

            response = JsonResponse({'success':True,'code': 0,'message':'pass','nickname':nickname,'sessionid':session_key,'id':id})
            response["Access-Control-Allow-Origin"] = "http://.alv.pub"
            response["Access-Control-Allow-Headers"] = "*"
            response["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            response["Access-Control-Allow-Credentials"] = 'true'

            return response
        else:
            response =  JsonResponse({'success': False,'code':1,'message':'Username or password error.'})
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Headers"] = "*"
            return response
    else:
        return JsonResponse({'success': False,'code':2,'message':'username and password can not bee null'})
@loginValid
def user_info(request):
    userid=request.session['user_id']
    user=User.objects.filter(id=userid)[0]
    nickname = user.nickname
    username= user.username
    email= user.email
    birthday = user.birthday
    if user:
        return JsonResponse({'code':0,'username':username,'nickname':nickname,'email':email,'birthday':birthday})
    else:
        return JsonResponse({'code': 1,'username':username, 'nickname': nickname, 'email': email, 'birthday': birthday})

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
    username = User.objects.filter(id=request.session['user_id'])[0].username
    file_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'files', username)
    if os.path.exists(file_dir):
        pass
    else:
        os.mkdir(file_dir)
    userfiles = os.listdir(file_dir)
    # cpassword='aaaa'
    users_role=User.objects.all()
    return render_to_response('content_template1.html', locals())

@loginValid
def get_weather_api(request):
    weatherStatus = get_weather.get_status()
    weatherMax = get_weather.get_max_temperature()
    weatherMin = get_weather.get_min_temperature()
    return JsonResponse({'success': True,'code':0,'weatherMin':weatherMin,'weatherMax':weatherMax,'weatherStatus':weatherStatus,'city':'上海'})



@loginValid
def new_account(request):
    all_account = Account.objects.filter(uid=request.session['user_id'])
    return render_to_response("new_account.html", locals())

@loginValid
def new_account_api(request):
    try:
        if request.method == 'POST' and request.POST:
            a = Account()
            id = uuid.uuid1()
            a.id = id
            a.username = request.POST['username']
            a.password = request.POST['password']
            a.application = request.POST['application']
            a.comment = request.POST['comment']
            a.uid = request.session['user_id']
            a.save()
            updateDate = Account.objects.get(id=id).updateDate.strftime('%Y-%m-%d %H:%M:%S')
            return JsonResponse({'success': True,'code':0,'message':'保存成功。','updateDate':updateDate,'id':str(id)})
        else:
            return JsonResponse({'success': False,'code':1,'message':'保存失败，仅支持post请求。'})
    except Exception as e:
        return  JsonResponse({'success': False,'code':2,'message':e})


@loginValid
def confirm_userinfo_change_api(request):
    try:
        if request.method == 'POST' and request.POST:

            # t = User()
            t = User.objects.get(id=request.session['user_id'])
            t.username = request.POST['username']
            t.nickname = request.POST['nickname']
            t.email = request.POST['email']
            # t.birthday = request.POST['birthday']
            t.save()
            return JsonResponse({'success': True,'code':0,'message':'保存成功。','nickname':request.POST['nickname']})
        else:
            return JsonResponse({'success': False,'code':1,'message':'保存失败，仅支持post请求。'})
    except Exception as e:
        return  JsonResponse({'success': False,'code':2,'message':e})


@loginValid
def change_vpntype_api(request):
    try:
        if request.method == 'POST' and request.POST:
            role = User.objects.get(id=request.session['user_id']).role
            if role == 1:
                if request.POST['vpn_type']== 'ipsec':
                    subprocess.call('sudo docker stop ikev2-vpn-server', shell=True)
                    subprocess.call('sudo docker start ipsec-vpn-server', shell=True)
                    response = JsonResponse({'success': True, 'code': 0, 'message': '现在开始使用ipsec/l2tp vpn' })
                    response["Access-Control-Allow-Origin"] = "*"
                    response["Access-Control-Allow-Headers"] = "*"
                    return response
                elif request.POST['vpn_type']== 'ikev2':
                    subprocess.call('sudo docker stop ipsec-vpn-server', shell=True)
                    subprocess.call('sudo docker start ikev2-vpn-server', shell=True)
                    response = JsonResponse({'success': True, 'code': 0, 'message': '现在开始使用ikev2 vpn'})
                    response["Access-Control-Allow-Origin"] = "*"
                    response["Access-Control-Allow-Headers"] = "*"
                    return response

                else:
                    return JsonResponse({'success': True, 'code': 1, 'message': '没有做任何变更操作。'})
            else:
                code=1
                message = 'what? 小伙子你没有权限访问这个的，我在后端还会再校验的，你别瞎搞。'
                return JsonResponse({'success': False, 'code': code, 'message': message})
        else:
            return JsonResponse({'success': False,'code':1,'message':'仅支持post请求。'})
    except Exception as e:
        return  JsonResponse({'success': False,'code':2,'message':e})

@loginValid
def update_code_api(request):
    try:
        if request.method == 'GET':
            role = User.objects.get(id=request.session['user_id']).role
            if role == 1:
                os.chdir('/home/alvin/ophira')
                subprocess.call('/usr/bin/git pull', shell=True)
                message = '已更新'
                code=0
            else:
                code=1
                message = 'what? 小伙子你没有权限访问这个的，我在后端还会再校验的，你别瞎搞。'
            return JsonResponse({'success': False,'code':code,'message':message})
        else:
            return JsonResponse({'success': False, 'code': 1, 'message': '请使用GET请求'})
    except Exception as e:
        return  JsonResponse({'success': False,'code':2,'message':e})

@loginValid
def upload_ajax_api(request):
    try:
        if request.method == 'POST':
            username = User.objects.filter(id=request.session['user_id'])[0].username
            file_obj = request.FILES.get('file')
            file_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'static','files',username)

            f = open(os.path.join(file_dir,file_obj.name), 'wb')
            # print(file_obj,type(file_obj))
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            # print('11111')
            return JsonResponse({'success': False, 'code': 0, 'message': '上传成功'})
        else:
            return JsonResponse({'success': False, 'code': 1, 'message': '请使用POST请求'})
    except Exception as e:
        return  JsonResponse({'success': False,'code':2,'message':e})

@loginValid
def delete_user_files(request):
    try:
        if request.method == 'POST':
            username = User.objects.filter(id=request.session['user_id'])[0].username
            filename = request.POST['filename']
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'files', username,filename)

            if os.path.exists(file_path):
                os.remove(file_path)
                if os.path.exists(file_path):
                    return JsonResponse({'success': False, 'code': 1, 'message': '删除失败'})
                else:
                    return JsonResponse({'success': False, 'code': 0, 'message': '删除成功'})
            else:
                return JsonResponse({'success': False, 'code': 1, 'message': '文件不存在。'})
        else:
            return JsonResponse({'success': False, 'code': 1, 'message': '请使用POST请求'})
    except Exception as e:
        return  JsonResponse({'success': False,'code':2,'message':e})


@loginValid
def delete_user_accounts_api(request):
    try:
        if request.method == 'POST':
            if request.POST['id'] == '000000':
                return JsonResponse({'success': False, 'code': 1, 'message': '新添加的账号请刷新当前页面后再删除。'})
            a = Account.objects.filter(uid=request.session['user_id'],id=request.POST['id'])
            if len(a) == 0:
                return JsonResponse({'success': False, 'code': 1, 'message': '该记录已不存在'})
            else:
                a.delete()
                if len(a) == 0:
                    return JsonResponse({'success': False, 'code': 0, 'message': '删除成功'})
                else:
                    return JsonResponse({'success': False, 'code': 1, 'message': '删除失败。'})
        else:
            return JsonResponse({'success': False, 'code': 1, 'message': '请使用POST请求'})
    except Exception as e:
        return  JsonResponse({'success': False,'code':2,'message':e})

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
    response =  render_to_response('reqTest.html',locals())
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "*"
    response["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    response["Access-Control-Allow-Credentials"] = 'true'
    return response


def ip(request):
    ip = client_ip(request)
    return render_to_response('ip.html',locals())


def register_api(request):
    try:
        if request.method == 'POST' and request.POST:
            try:
                if User.objects.get(username=request.POST['username']):
                    return JsonResponse({'code': 1, 'message': '注册失败，用户名已存在，请使用其他用户名。'})
            except:
                import re
                if re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',request.POST['email']):
                    if request.POST['birthday'] != '':
                        u = User()
                        u.username = request.POST['username']
                        u.password = hashpassword(request.POST['password'])
                        u.email = request.POST['email']
                        u.nickname = request.POST['nickname']
                        u.birthday = request.POST['birthday']
                        u.id = uuid.uuid1()
                        u.save()
                        return JsonResponse({'success': True, 'code': 0, 'message': '注册成功'})
                    else:
                        return JsonResponse({'success': True, 'code': 1, 'message': '请选择日期'})
                else:
                    return JsonResponse({'code': 1, 'message': '请正确的填写邮箱。'})
        else:
            return JsonResponse({'success': False, 'code': 1, 'message': '请正确填写全部信息'})
            # return JsonResponse({'success': False, 'code': 1, 'message': request.POST})

    except Exception as e:
        return JsonResponse({'success': False, 'code': 2, 'message': e})

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
    try:
        last_name=request.session['name']
        last_password=request.session['password']
    except:
        pass
    now=time.strftime('%Y-%m-%d %H:%M:%S')
    request.session['name'] = 'diana'+now
    request.session['password'] = 'wankaihao'+now
    new_name=request.session['name']
    new_password=request.session['password']

    key=request.session.session_key
    # key=type(t1_key)

    return render_to_response('testSession.html',locals())


def blogroll(request):
    return render_to_response('blogroll.html',locals())

def frame_test(request):
    return render_to_response('frame_test.html',locals())

def iview_test(request):
    return render_to_response('iview_test.html',locals())

@loginValid
def change_password(request):
    try:
        userid = request.session['user_id']
        user = User.objects.filter(id=userid)[0]
        if request.method == 'POST' and request.POST:
            oldpasswd = hashpassword(request.POST['oldpasswd'])
            passwd = hashpassword(request.POST['passwd'])
            passwdCheck = hashpassword(request.POST['passwdCheck'])
            if passwd == passwdCheck:
                if len(request.POST['passwd']) < 6:
                    return JsonResponse({'success': False, 'code': 4, 'message': '密码长度少于6'})
                else:
                    if oldpasswd == user.password:
                        u=User.objects.get(id=userid)
                        u.password=passwd
                        u.save()
                        return JsonResponse({'success': True,'code':0,'message':'success'})
                        exit(0)
                    else:
                        return JsonResponse({'success': False,'code':1,'message':'authentication failed'})
            else:
                return JsonResponse({'success': False, 'code': 3, 'message': '两次输入的密码不一样'})
        else:
            return JsonResponse({'success': False, 'code': 5, 'message': '只支持post请求'})
    except Exception as e:
        return JsonResponse({'success': False,'code':2,'message':e})


def new_login(request):
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

def vuetest(request):
    message='django message'
    return render_to_response('vuetest.html',locals())

def new_template1(request):
    return render_to_response('content_template1.html', locals())