"""ophira URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from sophiroth.views import *
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^reqTest/',reqTest),
    url(r'^ip', ip),
    url(r'^register',register),
    url(r'^testcookie',testcookie),
    url(r'^testsission', testsission),
    url(r'^na',new_account),
    url(r'^login',new_login),
    url(r'^logout$',logout),
    url(r'blogroll',blogroll),
    url(r'frame_test', frame_test),
    url(r'iview_test',iview_test),
    url(r'change_password',change_password),
    url(r'jstest$',jstest),
    url(r'jstest1', jstest1),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'/static/img/favicon.ico')),
    url(r'^jqajax',jqajax_test),
    url(r'^jquery_test', jquery_test),
    url(r'auth_pass',auth_pass),
    url(r'vuetest', vuetest),
    url(r'user_info',user_info),
    url(r'^new_template1',new_template1),
    url(r'^new_account_api',new_account_api),
    url(r'^api/register',register_api),
    url(r'^api/confirm_userinfo_change_api',confirm_userinfo_change_api),
    url(r'^api/change_vpntype_api',change_vpntype_api),
    url(r'^api/update_code_api',update_code_api),
    url(r'^api/upload_ajax_api',upload_ajax_api),
    url(r'^api/delete_user_files',delete_user_files),
    url(r'^api/delete_user_accounts_api',delete_user_accounts_api),
    url(r'^api/get_weather_api',get_weather_api),
]
