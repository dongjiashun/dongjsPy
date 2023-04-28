# -*- coding: UTF-8 -*- 
import MySQLdb
from django.conf import settings
from .MyLogger import logger
import traceback

class InceptionResultDao(object):
    def __init__(self):
        try:
            # dev
            # self.host = 'rm-bp188fb70hknd9gi2o.mysql.rds.aliyuncs.com'
            # self.port = 3306
            # self.user = 'devuser'
            # self.passwd='Devuser123'
            # self.db = 'dms'

            # pro
            self.host = '127.0.0.1'
            self.port = 3306
            self.user = 'root'
            self.passwd = 'p7amA5FEXJcDSjOQ'
            self.db = 'dms3'
        except Exception as a:
            trace_message = traceback.format_exc()
            logger.warn("InceptionResultDao init error:\n" + trace_message)



    def query(self,hash):
        result = None
        conn = None
        cur = None
        try:
            conn = MySQLdb.connect(host=self.host,
                           user=self.user,
                           passwd=self.passwd,
                           db=self.db,
                           port=self.port,
                           charset='utf8')

            cur = conn.cursor()
            select_sql = "select * from inception_result where hash='%s'" % (hash)
            ret = cur.execute(select_sql)
            conn.commit()
            result = cur.fetchall()
        except MySQLdb.Error as e:
            trace_message = traceback.format_exc()
            logger.error("inception or mysql error:\n" + trace_message)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return result



    def insert_or_update(self,hash , value):
        if hash == "":
            return None
        result = None
        conn = None
        cur = None
        try:
            conn = MySQLdb.connect(host=self.host,
                                   user=self.user,
                                   passwd=self.passwd,
                                   db=self.db,
                                   port=self.port,
                                   charset='utf8')

            cur = conn.cursor()
            result = self.query(hash)
            # 如果已经有这样一条记录
            if len(result) > 0:
                insert_sql = 'update inception_result set result="%s" where hash="%s"' % (value, hash)
            else:
                insert_sql = 'insert into inception_result (hash,result) values("%s","%s")' % (hash, value)
            ret = cur.execute(insert_sql)
            conn.commit()
            result = cur.fetchall()
        except MySQLdb.Error as e:
            trace_message = traceback.format_exc()
            logger.error("inception or mysql error:\n" + trace_message)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return result
