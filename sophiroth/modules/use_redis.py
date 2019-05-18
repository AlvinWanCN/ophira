#coding:utf-8

from django.core.cache import cache
from django.shortcuts import render_to_response
from sophiroth.models import *
import json,time
import logging,os
filename=filename=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'logs','ophira.log')
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename=filename)
logger = logging.getLogger('ophira')

def use_redis(DATA_TABLE,HTML_KEY,HTML_NAME,request):
    start = time.clock()
    account_data=[];
    UNIQ_TABLE_GROUP={}
    TABLE_GROUP_DATA = [];
    try:
        if cache.has_key(HTML_KEY):
            response=cache.get(HTML_KEY)
            logger.info(HTML_KEY + ' have response cache in redis.')
            logger.info('This response collect used time: %s Seconds' % (time.clock() - start))
            return response
        else:
            logger.info(HTML_KEY + ' have not response cache in redis.')
            try:
                if cache.has_key(DATA_TABLE): #判断是否有关于数据的缓存，有则直接从redis缓存里读取，没有则去mysql数据库查询。
                    logger.info(DATA_TABLE + ' have data cache in redis')
                    if DATA_TABLE == 'account':
                        account=cache.get(DATA_TABLE)
                else:
                    if DATA_TABLE == 'account':
                        account=Account.objects.filter(uid=request.session['user_id'])
                        cache.set(DATA_TABLE, account, 365 * 24 * 60 * 60)
            except Exception as e: #如果查询或设置缓存的过程中出现异常，则直接从mysql数据库里获取数据传给前端。
                logger.error('Get or set redis cache get exception,Now query direct. Exception content:' + e)
                if DATA_TABLE == 'account':
                    account = Account.objects.filter(uid=request.session['user_id'])

            for i in cache.get(DATA_TABLE):
                if UNIQ_TABLE_GROUP.has_key(i.group.encode("utf-8")):
                    pass
                else:
                    GROUP_NAME = i.group.encode("utf-8")
                    TABLE_GROUP_DATA.append({'label': GROUP_NAME, 'value': GROUP_NAME})
                    UNIQ_TABLE_GROUP[GROUP_NAME] = GROUP_NAME
                try:
                    account_data.append({"group":i.group.encode("utf-8"),"application":i.application.encode("utf-8"),"username":i.username.encode("utf-8"),"password":i.password.encode("utf-8"),"comment":i.comment.encode("utf-8"),"id":i.id.encode("utf-8") })
                    #"updateDate":i.updateDate,
                except Exception as e:
                    logger.error('We have exception:' + str(e))
                    break
            response = render_to_response(HTML_NAME, locals())  #生成response内容。
            cache.set(HTML_KEY,response,365*24*60*60)  #将response内容设置到缓存。
    except Exception as e:
        logger.error('Exception for use reids:' + str(e))
        account = Account.objects.filter(uid=request.session['user_id'])
        cache.set(DATA_TABLE, account, 365 * 24 * 60 * 60)
        for i in cache.get(DATA_TABLE):
            if UNIQ_TABLE_GROUP.has_key(i.group.encode("utf-8")):
                pass
            else:
                GROUP_NAME = i.group.encode("utf-8")
                TABLE_GROUP_DATA.append({'label': GROUP_NAME, 'value': GROUP_NAME})
                UNIQ_TABLE_GROUP[GROUP_NAME] = GROUP_NAME
            try:
                account_data.append(
                    {"group":i.group.encode("utf-8"),"application": i.application.encode("utf-8"), "username": i.username.encode("utf-8"),
                     "password": i.password.encode("utf-8"), "comment": i.comment.encode("utf-8"), "id": i.id.encode("utf-8")})
            except Exception as e:
                logger.error('We have exception:' + str(e))
                break
        response = render_to_response(HTML_NAME, locals())
        logger.info('This response collect used time: %s Seconds' % (time.clock() - start))
    logger.info('This response collect used time: %s Seconds' % (time.clock() - start))
    return response