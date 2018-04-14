from django.shortcuts import render_to_response
from sophiroth.models import *
import hashlib
import modules.get_weather as  get_weather
from django.http import JsonResponse

# Create your views here.




def base(request):
    return render_to_response('base.html',locals())

def main_page(request):
    if request.method == "POST" and request.POST:
        nowTime=time.strftime('%Y-%m-%d %H:%M:%S')
        weatherStatus = get_weather.get_status()
        weatherMax = get_weather.get_max_temperature()
        weatherMin = get_weather.get_min_temperature()

        return render_to_response('main_content.html', locals())
    return render_to_response('main.html',locals())

def reqTest(request):
    return render_to_response('reqTest.html',locals())

def ip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return render_to_response('ip.html',locals())