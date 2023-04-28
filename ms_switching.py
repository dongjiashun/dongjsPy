# -*- coding: utf-8 -*-
from django.http import HttpResponse
import MySQLdb
import time
import sys
import json
class m_s:
    def __init__(self,host,user,password,port):
        self.host=host
        self.user=user
        self.passowrd=password
        self.port=port
    def getConn(self,db="mysql"):
        try:
            conn=MySQLdb.connect(host=self.host, user=self.user, passwd=self.passowrd, db=db, port=self.port, charset="utf8")
            cur = conn.cursor()
            return cur
        except Exception as e:
            return e
    def execSQLlock(self,*args):
        cur = args[0]
        flush_sql="FLUSH TABLES WITH READ LOCK"
        cur.execute(flush_sql)
    def execIo(self,cur,command):
        cur.execute(command)
        db_pos = cur.fetchall()
        for value in db_pos:
            value=value
        return value
    def exeStop(self,cur,command):
        cur.execute(command)
        db_pos = cur.fetchall()
        return db_pos
    def execSQLstatus(self,*args):
        cur = args[0]
        n=0
        self.execSQLlock(cur)
        flush_m = "flush logs"
        cur.execute(flush_m)
        while True:
            data=[]
            slave_pos=[]
            n=n+1
            exe_sql = "select Command,State,Info,Id from information_schema.processlist"
            cur.execute(exe_sql)
            plist = cur.fetchall()
            for li in range(len(plist)):
                if plist[li][0] == "Query" and plist[li][1] == "Waiting for global read lock":
                    lock_id = "kill " + str(plist[li][3])
                    print plist[li][2]
                    cur.execute(lock_id)
            slave_pos.append(self.execIo(cur1, "show master status")[1])
            data.append(self.execIo(cur1,"show slave status")[6]) ##从库的游标
            time.sleep(1)
            slave_pos.append(self.execIo(cur1, "show master status")[1])
            data.append(self.execIo(cur,"show master status")[1])##从库的游标
            print ".......",data,slave_pos
            if data[0]==data[1] and slave_pos[0]==slave_pos[1]:
                try:
                    print "第%s次判断数据已经同步....."%n
                    if n==c_time:
                        print "开始主从切换工作........"
                        self.exeStop(cur1,"stop slave") ##停止从库同步
                        new_pos=self.exeStop(cur1,"show master status")#获取新主库的FILE和POS的值,游标为还没切换前的从库
                        #print "获取新主库的FILE和POS的值,游标为还没切换前的从库",new_pos
                        self.exeStop(cur,"reset master;")##主库释放从库主从信息......
                        ##在从库执行new_change 指向新的主库
                        self.exeStop(cur1,"reset slave all")
                        new_change="change master to master_host='"+str(args[1])+"'"+",master_user='"+args[2]+"'"+",master_password='"+args[3]+"',master_port="+str(args[4])+",MASTER_LOG_FILE='"+str(new_pos[0][0])+"'"+",MASTER_LOG_POS="+str(new_pos[0][1])
                        print new_change
                        self.exeStop(cur,new_change)##在原来主库上执行change master to.....
                        #print "在原来主库上执行change master to...."
                        self.exeStop(cur,"start slave")  ##在原来主库上执行change master to.....
                        time.sleep(5)
                        s_pos=self.exeStop(cur,"show slave status;")
                        #print s_pos[0][10],s_pos[0][11]
                        if s_pos[0][10]=="Yes" and s_pos[0][11]=="Yes":
                            self.exeStop(cur1,"reset slave all")
                            print  "主从切换成功!"
                            message = {"messages":"success"}
                            return message
                            print "\n"
                            while True:
                                print "等待其他操作完成,即将unlock tables主库......"
                                try:
                                    stop = "q"
                                    if stop == "q":
                                        sys.exit()
                                        # break
                                except Exception as e:
                                    print "good bye"

                        else:
                            print   s_pos[0][19]
                        break
                except Exception as e:
                    return e
            else:
                print "主从数据未达到一致性..........",n
                n=0
                data=[]

def ms_switching(request):
    #sql = request.POST['archer']
    #ds = request.POST['ds']
    global c_time
    c_time = 10
    #c_time = request.GET.get('execu_time').encode('utf-8')
    print "****************************************************\n"
    print "请根据提示输入指定信息:"
    m_host = request.GET.get('master_url').encode('utf-8')
    m_user = request.GET.get('master_name').encode('utf-8')
    m_password = request.GET.get('master_pwd').encode('utf-8')
   # m_host = "192.168.171.133"
   # m_user = "root"
   # m_password = "s3kr1t"
    m_port = int(request.GET.get('master_port').encode('utf-8'))
    print "****************************************************\n"
    s_host = request.GET.get('slave_url').encode('utf-8')
    s_user = request.GET.get('slave_name').encode('utf-8')
    s_password = request.GET.get('slave_pwd').encode('utf-8')
    #s_host = "192.168.171.141"
    #s_user = "root"
    #s_password = "ht123qwasz%$x"
    s_port =  int(request.GET.get('slave_port').encode('utf-8'))
    M = m_s(m_host, m_user, m_password, m_port)
    S = m_s(s_host,s_user,s_password,s_port)
    global cur
    global cur1
    cur = M.getConn()  ##获取主库游标
    cur1 = S.getConn()  ##获取从库游标
    print "*****************************************************\n"
    print "主从同步用户信息.........\n"
    s_user1 = request.GET.get('syn_name').encode('utf-8')
    s_password1 = request.GET.get('syn_pwd').encode('utf-8')
    s_port1 = int(request.GET.get('syn_port').encode('utf-8'))
    opt_result = {"messages":"success"}
    #progress_result = json.dumps(opt_result)
    ms_message = M.execSQLstatus(cur,s_host,s_user1,s_password1,s_port1)
    progress_result = json.dumps(ms_message)
    return  HttpResponse(progress_result, content_type='application/json')

if __name__ =="__main__":
    c_time=1
    print "****************************************************\n"

    print "请根据提示输入指定信息:"
    m_host = "192.168.171.141"
    m_user = "root"
    m_password = "ht123qwasz%$x"
  # m_host = "192.168.171.133"
  # m_user = "root"
  # m_password = "s3kr1t"
    m_port = 3306
    print "****************************************************\n"
    s_host = "192.168.171.133"
    s_user = "root"
    s_password = "s3kr1t"
   #s_host = "192.168.171.141"
   #s_user = "root"
   #s_password = "ht123qwasz%$x"
    s_port = 3306
    M = m_s(m_host, m_user, m_password, m_port)
    S = m_s(s_host,s_user,s_password,s_port)
    global cur
    global cur1
    cur = M.getConn()  ##获取主库游标
    cur1 = S.getConn()  ##获取从库游标
    print "*****************************************************\n"
    print "主从同步用户信息.........\n"
    s_user1 = "htslave"
    s_password1 = "htslave123456"
    s_port1 = 3306

    ms_message = M.execSQLstatus(cur,s_host,s_user1,s_password1,s_port1)
    print ms_message
