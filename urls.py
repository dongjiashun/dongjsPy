# -*- coding: UTF-8 -*- 
from django.conf.urls import patterns, include, url
from . import view
from . import http_process# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dongjs_last.views.home', name='home'),
    # url(r'^dongjs_last/', include('dongjs_last.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', view.hello),
    url(r'^calc/$', view.calc, name='dongjscalc'),
    url(r'^api/check$', http_process._sql_check, name='sql_check'),
    url(r'^api/execute$', http_process._sql_execute, name='sql_execute'),
    url(r'^api/epoll$', http_process._sql_async_execute, name='sql_async_execute'),
    url(r'^api/progress$', http_process._get_osc_percent, name='get_osc_percent'),
    url(r'^api/cancelprogress$', http_process._stop_osc, name='stop_osc'),
    
    ##测试 dms调用python接口是否连通 接口
    url(r'^api/dongjs$', http_process.dongjs, name='dongjs')
)
