# -*- coding: UTF-8 -*- 
import re
import json
import MySQLdb
import traceback
import threading

from dongjsPy.settings import *
from dongjsPy.global_params import local_inception
from dongjsPy.inception_result_dao import InceptionResultDao
from dongjsPy.MyLogger import logger
from dongjsPy.result_model import ProgressResult,Result
from django.conf import settings

from dongjsPy.Constant import SqlType
from dongjsPy import *

# tmp_async_execute_process = {}
inception_result = InceptionResultDao()

class Service(object):
    def __init__(self):
        try:
            self.inception_check_params = "--enable-check=1;--enable-ignore-warnings;";
            self.inception_split_params = "--enable-split;--enable-execute;";
            self.inception_execute_params = "--enable-execute;--enable-ignore-warnings;--disable-remote-backup;";

            self.inception_host = getattr(settings, 'INCEPTION_HOST')
            self.inception_port = int(getattr(settings, 'INCEPTION_PORT'))

            self.inception_remote_backup_host = getattr(settings, 'INCEPTION_REMOTE_BACKUP_HOST')
            self.inception_remote_backup_port = int(getattr(settings, 'INCEPTION_REMOTE_BACKUP_PORT'))
            self.inception_remote_backup_user = getattr(settings, 'INCEPTION_REMOTE_BACKUP_USER')
            self.inception_remote_backup_password = getattr(settings, 'INCEPTION_REMOTE_BACKUP_PASSWORD')
        except Exception as a:
            trace_message = traceback.format_exc()
            logger.warn("Service init error:\n" + trace_message)

    def _do_execute(self , target_execute_sql):
        result = None
        conn = None
        cur = None
        print local_inception.inception_host
        print local_inception.inception_port
        try:
            
            conn=MySQLdb.connect(host=local_inception.inception_host, user='root', passwd='', db='', port=local_inception.inception_port)
           # conn = MySQLdb.connect(host='192.168.203.129',user='root',passwd='',db='',port=6669,,use_unicode=True)
            #execute_sql = target_execute_sql.encode("utf-8")
#                    db = self._get_db()
            execute_sql = target_execute_sql.encode('utf-8')  
            cur=conn.cursor()
            ret=cur.execute(execute_sql)
            result=cur.fetchall()
        except MySQLdb.Error as e:
            trace_message = traceback.format_exc()
            logger.error("inception or mysql error:\n" + trace_message)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return result

    def _get_target_sql(self,sql,ds,type):
        target_value = re.split(':',ds);
        host = target_value[0]
        port = target_value[1]
        db_name = target_value[2]
        user_name = target_value[3]
        user_password = target_value[4]
        inception_sql_to_execute = self._sql_to_inceptionsql(sql,host,port,db_name,user_name,user_password,type)
        return inception_sql_to_execute;

    def _sql_to_inceptionsql(self,sql,host,port,db_name,user_name,user_password,type):
        # if type == SqlType.split:
        #     newsql = "use " + db_name+";\n"+archer
        # else:
        #     newsql = archer

        newsql = "use " + db_name + ";\n" + "set names utf8mb4;\n"+sql
        inception_sql = '';
        # type=0,1,2��0����split,1����check,2����execute
        if type == SqlType.split:
            inception_sql = "/*--user=%s;--password=%s;--host=%s;--port=%s;--enable-execute;--enable-split;--enable-ignore-warnings;--disable-remote-backup;*/\
                            inception_magic_start;\
                            %s\
                            inception_magic_commit;" % (user_name, user_password, host, str(port),newsql)
        elif type == SqlType.check:
            inception_sql = "/*--user=%s;--password=%s;--host=%s;--port=%s;--enable-check=1;--disable-remote-backup;*/\
                                        inception_magic_start;\
                                        %s\
                                        inception_magic_commit;" % (user_name, user_password, host, str(port), newsql)
        elif type == SqlType.execute:
            inception_sql = "/*--user=%s;--password=%s;--host=%s;--port=%s;--enable-execute;--enable-ignore-warnings;--disable-remote-backup;*/\
                                        inception_magic_start;\
                                        %s\
                                        inception_magic_commit;" % (user_name, user_password, host, str(port), newsql)

        elif type == SqlType.async_execute:
            inception_sql = "/* --user=%s;--password=%s;--host=%s;--port=%s;--enable-execute;--enable-ignore-warnings;--disable-remote-backup;*/\
                                                    inception_magic_start;\
                                                    %s\
                                                    inception_magic_commit;" % (
            user_name, user_password, host, str(port), newsql)

        return inception_sql

    def _sql_split(self,sql,ds):
        target_execute_sql = self._get_target_sql(sql,ds,SqlType.split)
        split_sql = self._do_execute(target_execute_sql)
        return split_sql

    def _sql_check(self,sql,ds):
        json_string = ''
        result_list = []
        try:
            # split_sql = self._sql_split(archer,ds)
            # logger.info("_sql_check split���sql:\n" + split_sql)
            # for split_one_sql in split_sql:
                # one_part_sql = split_one_sql[1]
            one_part_target_execute_sql = self._get_target_sql(sql,ds,SqlType.check)
            results = self._do_execute(one_part_target_execute_sql)
            for result in results:
                result_object = Result()
                result_object.errlevel = result[2]
                result_object.SQL = result[5]
                result_object.errormessage = result[4]
                result_object.Affected_rows = result[6]
                result_object.execute_time = result[9]
                result_object.stagestatus = result[3]
                result_list.append(result_object)
            json_string = json.dumps([ob.__dict__ for ob in result_list])
        except BaseException as e:
            trace_message = traceback.format_exc()
            logger.warn("_sql_check fail:\n"+trace_message)
        return json_string

    # ��ȡÿ��ִ�е�sql��Ӧ��sha_hash���п���û�ж�Ӧ��sha_hash��û�еĻ�ֱ������
    def _sql_get_sha(self,sql,ds):
        sha_list = []
        try:
            # split_sql = self._sql_split(archer, ds)
            # for split_one_sql in split_sql:
            #     one_part_sql = split_one_sql[1]
            one_part_target_execute_sql = self._get_target_sql(sql, ds, SqlType.check)
            results = self._do_execute(one_part_target_execute_sql)
            for result in results:
                # result��tuple�������Ԫ�س�����11�����һ����sha_hashֵ
                if result.__len__() < 11:
                    continue
                a_hash = result[10]
                if a_hash != "":
                    sha_list.append(a_hash)
        except BaseException as e:
            trace_message = traceback.format_exc()
            logger.error("_sql_get_sha fail:\n" + trace_message)
        return sha_list

    def _sql_execute(self, sql, ds):
        json_string = ''
        result_list = []
        try:
            # split_sql = self._sql_split(archer,ds)
            # for split_one_sql in split_sql:
            #     one_part_sql = split_one_sql[1]
            one_part_target_execute_sql = self._get_target_sql(sql,ds,SqlType.execute)

            # log
            # tmp_target = one_part_target_execute_sql
            # tmp_target = re.sub(r'(user=)([a-zA-Z0-9]+)', "******", tmp_target, re.M | re.I)
            # tmp_target = re.sub(r'(password=)([a-zA-Z0-9]+)', "******", tmp_target, re.M | re.I)
            # logger.info("target _sql_execute archer = " + tmp_target)

            results = self._do_execute(one_part_target_execute_sql)
            for result in results:
                result_object = Result()
                result_object.errlevel = result[2]
                result_object.SQL = result[5]
                result_object.errormessage = result[4]
                result_object.Affected_rows = result[6]
                result_object.execute_time = result[9]
                result_object.stagestatus = result[3]
                result_list.append(result_object)
            json_string = json.dumps([ob.__dict__ for ob in result_list])
        except BaseException as e:
            trace_message = traceback.format_exc()
            logger.warn("_sql_execute fail:\n" + trace_message)
        return json_string

    def _sql_async_execute(self, sql, ds, sha_list, env):
        if env == "true":
            local_inception.inception_host = INCEPTION_HOST
            local_inception.inception_port = int(INCEPTION_PORT)
        else:
            local_inception.inception_host = TEST_INCEPTION_HOST
            local_inception.inception_port = int(TEST_INCEPTION_PORT)

        logger.info(threading.current_thread().name+" start async execute sha_list = %s" % (json.dumps(sha_list)) +"\nsql = %s" % (sql))
        try:
            # split_sql = self._sql_split(archer, ds)
            # for split_one_sql in split_sql:
            #     one_part_sql = split_one_sql[1]
            one_part_target_execute_sql = self._get_target_sql(sql, ds, SqlType.async_execute)
            # log
            # tmp_target = one_part_target_execute_sql
            # tmp_target = re.sub(r'(user=)([a-zA-Z0-9]+)', "******", tmp_target, re.M | re.I)
            # tmp_target = re.sub(r'(password=)([a-zA-Z0-9]+)', "******", tmp_target, re.M | re.I)
            # logger.info("target _sql_async_execute archer = " + tmp_target)


            # ���ڴ��ı�������ﻨ��ʱ���ܳ�����inception��������Ż�
            results = self._do_execute(one_part_target_execute_sql)

            if results is None or len(results) <= 0:
                logger.error("�첽ִ����û���κν�����ֶ�д��dbÿ��hash�Ľ��״̬")
                for sha in sha_list:
                    inception_result.insert_or_update(sha, "manual finished")
            else:
                for result in results:
                    temp_async_result = str('archer = ' + str(result[5]).replace("\n","\\n") +' resultStatus = '+ str(result[3]).replace("\n","\\n")+' errormessage = '+ str(result[4])).replace("\n","\\n")
                    errormessage = result[4]
                    sha = result[10]
                    inception_result.insert_or_update(sha,temp_async_result)
                    # logger.info('archer = ' + result[5]+'\\n errormessage = '+result[4])

            result_str = json.dumps(results)
            logger.info("���len=" + str(len(results)) + " ִ�н��: " + result_str)
        except BaseException as e:
            trace_message = traceback.format_exc()
            logger.warn("_sql_async_execute fail:\n" + trace_message)
        logger.info(threading.current_thread().name+" finish async execute sha1 = %s" % (json.dumps(sha_list)))


    def _get_osc_percent(self, sql_sha1):
        json_string = ''
        try:
            progressResult = ProgressResult()
            sql_osc = "inception get osc_percent '%s'" % sql_sha1
            result = self._do_execute(sql_osc)
            if result is None or len(result) == 0:
                # tmp_msg = get_value_by_key(sql_sha1)
                # if tmp_msg is None:
                #     tmp_msg = 'task already complete or task not exist'
                result = inception_result.query(sql_sha1)
                tmp_msg = ""
                if result is not None and len(result) > 0:
                    # �����е�ֵ
                    tmp_msg = result[0][2]
                # tmp_msg = tmp_async_execute_process.get(sql_sha1, 'task already complete or task not exist')
                logger.info("tmp_msg="+tmp_msg)
                progressResult.messages = tmp_msg
                if "init" in tmp_msg:
                    progressResult.status = 0
                elif "Error" in tmp_msg or "Execute failed" in tmp_msg:
                    progressResult.status = 1
                else:
                    progressResult.status = 2
                # �����һ�η��ؽ�����ɾ��
                # self.del_previous_sha_if_exist(sql_sha1)
            else:
                process = result[0][3]
                if process < 100:
                    progressResult.status = 0
                    percent = result[0][3]
                    remaining_time = result[0][4]
                    # logger.info(sql_sha1+" ��Ӧ��״̬,")
                    # logger.info("percent = "+str(percent))
                    # logger.info("remaining_time = " + remaining_time)
                    temp_result = 'percent:%s, remaining_time:%s' % (percent, remaining_time)
                    progressResult.messages = temp_result

                elif process == 100:
                    progressResult.status = 2
                    allmessages = ''
                    for item in result[0]:
                        allmessages +=  str(item).replace("\n","\\n")
                        allmessages += '\\n'
                    progressResult.messages = allmessages
            json_string = progressResult.dump()
        except BaseException as e:
            trace_message = traceback.format_exc()
            logger.warn("_get_osc_percent fail:\n" + trace_message)
        return json_string

    # def del_previous_sha_if_exist(self,sql_sha1):
    #     not_exist = tmp_async_execute_process.get(sql_sha1, 'not_exist')
    #     if not_exist.__ne__('not_exist') & not_exist.__ne__('init'):
    #         del tmp_async_execute_process[sql_sha1]

    def stop_osc_progress(self, sql_sha1):
        """��֪SHA1ֵ������inception����ֹͣOSC���̣��漰��Inception�����ע�������ο�http://mysql-inception.github.io/inception-document/osc/"""
        sqlStr = "inception stop alter '%s'" % sql_sha1
        result = self._do_execute(sqlStr)
        if result is not None:
            opt_result = {"status":0, "messages":"�ɹ�ֹͣOSC����"}
        else:
            opt_result = {"status":1, "messages":"OSC���񲻴���"}
        return json.dumps(opt_result)

