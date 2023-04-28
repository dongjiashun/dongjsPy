#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import MySQLdb

 
sql= """
/*--user=mstdba_mgr;--password=8ffe3589337b7d35;--host=10.0.11.209;--port=3999;--enable-check=1;--disable-remote-backup;*/ 
inception_magic_start;
use redis_manager;
set names utf8mb4;
CREATE TABLE `redis_manager`.`new_table` (
  `idnew_table` INT NOT NULL DEFAULT 1 COMMENT '3',
  `new_tablecol` VARCHAR(45) NULL DEFAULT '3' COMMENT '3',
  `new_tablecol1` VARCHAR(45) NULL DEFAULT '1' COMMENT '34',
  PRIMARY KEY (`idnew_table`))
COMMENT = 'test';
inception_magic_commit;
"""
 
try:
    conn=MySQLdb.connect(host='192.168.131.128',
                         user='root',
                         passwd='',
                         db='',
                         port=6668)
    cur=conn.cursor()
    ret=cur.execute(sql)
    result=cur.fetchall()
    num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]
    print ' | '.join(field_names)
    for row in result:
        print ' | '.join([str(col) for col in row])
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    err_msg = 'Mysql Error {arg1}: {arg2}'.format(
                                     arg1 = e.args[0],
                                     arg2 = e.args[1])
    print err_msg