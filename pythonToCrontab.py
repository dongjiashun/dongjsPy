# -*- coding: UTF-8 -*- 
from crontab import CronTab
from django.http import HttpResponse
import json

def ptarchive(request): 
    print request
    jobdesc = request.GET.get('jobdesc').encode('utf-8')
    tport = request.GET.get('tport').encode('utf-8')
    tdatabase = request.GET.get('tdatabase').encode('utf-8')
    crontab = request.GET.get('crontab').encode('utf-8')
    tuser = request.GET.get('tuser').encode('utf-8')
    sdatabase = request.GET.get('sdatabase').encode('utf-8')
    surl = request.GET.get('surl').encode('utf-8')
    turl = request.GET.get('turl').encode('utf-8')
    suser = request.GET.get('suser').encode('utf-8')
    stable = request.GET.get('stable').encode('utf-8')
    ttable = request.GET.get('ttable').encode('utf-8')
    where = request.GET.get('where').encode('utf-8')
    sport = request.GET.get('sport').encode('utf-8')
    spwd = request.GET.get('spwd').encode('utf-8')
    tpwd = request.GET.get('tpwd').encode('utf-8')
    my_user_cron  = CronTab(user=True)
    #date = date 
    # 创建任务
    job = my_user_cron.new(command="sh  /home/dongjs/pt-archive/pt-archive_model.sh "+
                           " -a "+surl+
                           " -b "+sdatabase+
                           " -c "+suser+
                           " -d "+spwd+
                           " -e "+stable+
                           " -f "+turl+
                           " -g "+tdatabase+
                           " -i "+tpwd+
                           " -j "+ttable+
                           " -k "+where
                          )
    # 设置任务执行周期，每两分钟执行一次
    job.setall(crontab)
    # 同时可以给任务设置comment，这样就可以根据comment查询，很方便
    job.set_comment(jobdesc)
    # 根据comment查询，当时返回值是一个生成器对象，不能直接根据返回值判断任务是否#存在，如果只是判断任务是
    iter = my_user_cron.find_comment(jobdesc)
    # 任务的disable和enable， 默认enable
    print iter
    job.enable(False)
    job.enable()
    # 最后将crontab写入配置文件
    my_user_cron.write()
    message = {"messages":"success"}
    progress_result = json.dumps(message)
    return  HttpResponse(progress_result, content_type='application/json')