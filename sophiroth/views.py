from django.shortcuts import render_to_response
from sophiroth.models import *
import hashlib
from django.http import JsonResponse

# Create your views here.




def base(request):
    return render_to_response('base.html',locals())

def main_page(request):
    return render_to_response('main.html',locals())