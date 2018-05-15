#coding:utf-8

import subprocess
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import random
import platform

print()
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

@loginValid
def get_sys_state(request):
    try:
        if platform.system() == 'Linux':
            available_mem=int(subprocess.check_output('zabbix_get -s localhost -k vm.memory.size[available]', shell=True).split('\n')[0])/1024/1024
            total_mem=int(subprocess.check_output('zabbix_get -s localhost -k vm.memory.size[total]', shell=True).split('\n')[0])/1024/1024
            used_mem=total_mem-available_mem
            cpu_used=float('%.2f' % float(100-float(subprocess.check_output('zabbix_get -s localhost -k system.cpu.util[,idle]', shell=True).split('\n')[0])))
        else:
            available_mem = random.randint(100, 600)
            total_mem = 900
            used_mem = total_mem - available_mem
            cpu_used = random.randint(0,100)
    except Exception as e:
        available_mem=random.randint(100,600)
        total_mem=900
        used_mem = total_mem - available_mem
        cpu_used = random.randint(0, 100)
    return JsonResponse({'total_mem':total_mem,'available_mem':available_mem,'used_mem':used_mem,'cpu_used':cpu_used})