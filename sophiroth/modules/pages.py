#coding:utf-8
from django.shortcuts import render_to_response

def system_state(requst):
    return render_to_response('system_state.html', locals())