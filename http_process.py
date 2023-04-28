# -*- coding: UTF-8 -*- 
from django.http import HttpResponse

from dongjsPy.settings import *
from dongjsPy.global_params import local_inception
from dongjsPy.inception_result_dao import InceptionResultDao
from dongjsPy.service import Service
from dongjsPy.MyLogger import logger
import os
import threading
from dongjsPy import *
import json

service = Service()
inception_result = InceptionResultDao()

def _sql_check(request):
    sql = request.POST['archer']
    ds = request.POST['ds']
    env_is_online = request.POST.get('env', "true")
    change_inception(env_is_online)
    logger.info("_sql_check accept archer = %s" % (sql,))
    progressResult = service._sql_check(sql,ds);
    return HttpResponse(progressResult, content_type='application/json')


def _sql_execute(request):
    sql = request.POST['archer']
    ds = request.POST['ds']

    env_is_online = request.POST.get('env', "true")
    change_inception(env_is_online)

    # logger.info("_sql_execute accept archer = %s" % (archer,))
    progressResult = service._sql_execute(sql,ds)
    return HttpResponse(progressResult, content_type='application/json')


def _sql_async_execute(request):
    sql = request.POST['archer']
    ds = request.POST['ds']

    env_is_online = request.POST.get('env', "true")
    change_inception(env_is_online)

    # logger.info("_sql_async_execute accept archer = %s" % (archer,))
    sha_list = service._sql_get_sha(sql,ds)
    for sha in sha_list:
        #鍒濆鍖栫殑鏃跺�欐彃鍏nit
        inception_result.insert_or_update(sha, "init")
    async_thread = threading.Thread(target=service._sql_async_execute,args=(sql, ds, sha_list, env_is_online),name="async_execute_worker")
    async_thread.start()
    return HttpResponse(json.dumps(sha_list), content_type='application/json')


def _get_osc_percent(request):
    hash = request.POST['hash']

    env_is_online = request.POST.get('env', "true")
    change_inception(env_is_online)

    # logger.info("_get_osc_percent accept hash = %s" % (hash,))
    progress_result = service._get_osc_percent(hash)
    return HttpResponse(progress_result, content_type='application/json')


def _stop_osc(request):
    hash = request.POST['hash']

    env_is_online = request.POST.get('env', "true")
    change_inception(env_is_online)

    logger.info("_stop_osc accept hash = %s" % (hash,))
    progress_result = service.stop_osc_progress(hash)
    return HttpResponse(progress_result, content_type='application/json')


def change_inception(env_is_online):
    if env_is_online == "true":
        local_inception.inception_host = INCEPTION_HOST
        local_inception.inception_port = int(INCEPTION_PORT)
    else:
        local_inception.inception_host = TEST_INCEPTION_HOST
        local_inception.inception_port = int(TEST_INCEPTION_PORT)


def dongjs(request):
    sql = request.POST['archer']
    ds = request.POST['ds']
    print "dongjs success"
    env_is_online = request.POST.get('env', "true")
    change_inception(env_is_online)
    logger.info("dongjs accept archer = %s" % (sql,))
    progressResult = service._sql_check(sql,ds);
    return HttpResponse(progressResult, content_type='application/json')

