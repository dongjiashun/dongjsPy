#!/usr/bin/python
#coding:utf-8
 
import MySQLdb
import time,datetime
 
 
#zabbix数据库信息：
zdbhost = '10.77.64.60'
zdbuser = 'zabbix'
zdbpass = 'zabbix'
zdbport = 3306
zdbname = 'zabbix'

#生成文件名称：
xlsfilename = 'zabbix_db_report.xls'
 
#需要查询的key列表 [名称，表名，key值，取值，格式化，数据整除处理]
keys = [

    ['iops读最大值','trends_uint','custom.vfs.dev.read.ops[sda]','max','',1],
    ['iops读平均值','trends_uint','custom.vfs.dev.read.ops[sda]','avg','',1],
    ['iops写最大值','trends_uint','custom.vfs.dev.write.ops[sda]','max','',1],
    ['iops写平均值','trends_uint','custom.vfs.dev.write.ops[sda]','avg','',1]
    
]
 
 
class ReportForm:
 
    def __init__(self):
        '''打开数据库连接'''
        self.conn = MySQLdb.connect(host=zdbhost,user=zdbuser,passwd=zdbpass,port=zdbport,db=zdbname)
        self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
 
        #生成zabbix哪个分组报表
        self.groupname = 'DB'
 
        #获取IP信息：
        self.IpInfoList = self.__getHostList()
 
    def __getHostList(self):
        '''根据zabbix组名获取该组所有IP'''
 
        #查询组ID:
        sql = '''select groupid from groups where name = '%s' ''' % self.groupname
        self.cursor.execute(sql)
        groupid = self.cursor.fetchone()['groupid']
 
        #根据groupid查询该分组下面的所有主机ID（hostid）：
        sql = '''select hostid from hosts_groups where groupid = '%s' ''' % groupid
        self.cursor.execute(sql)
        hostlist = self.cursor.fetchall()
 
        #生成IP信息字典：结构为{'119.146.207.19':{'hostid':10086L,},}
        IpInfoList = {}
        for i in hostlist:
            hostid = i['hostid']
            sql = '''select host from hosts where status = 0 and hostid = '%s' ''' % hostid
            ret = self.cursor.execute(sql)
            if ret:
                #首先fetchone()函数它的返回值是单个的元组,也就是一行记录,如果没有结果,那就会返回null
                IpInfoList[self.cursor.fetchone()['host']] = {'hostid':hostid}
        return IpInfoList
 
    def __getItemid(self,hostid,itemname):
        '''获取itemid'''
        sql = '''select itemid from items where hostid = '%s' and key_ = '%s' ''' % (hostid, itemname)
        if self.cursor.execute(sql):
            itemid = self.cursor.fetchone()['itemid']
        else:
            itemid = None
        return itemid
 
    def getTrendsValue(self,type, itemid, start_time, stop_time):
        '''查询trends_uint表的值,type的值为min,max,avg三种'''
        sql = '''select %s(value_%s) as result from trends where itemid = '%s' and clock >= %s and clock <= %s ''' % (type, type, itemid, start_time, stop_time)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()['result']
        if result == None:
            result = 0
        return result
 
    def getTrends_uintValue(self,type, itemid, start_time, stop_time):
        '''查询trends_uint表的值,type的值为min,max,avg三种'''
        sql = '''select %s(value_%s) as result from trends_uint where itemid = '%s' and clock >= %s and clock <= %s ''' % (type, type, itemid, start_time, stop_time)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()['result']
        if result:
            result = int(result)
        else:
            result = 0
        return result
 
 
    def getLastMonthData(self,type,hostid,table,itemname):
        '''根据hostid,itemname获取该监控项的值'''
        #获取上个月的第一天和最后一天
        #ts_first = int(time.mktime(datetime.date(datetime.date.today().year,datetime.date.today().month-1,1).timetuple()))
        #lst_last = datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)
        ts_first = int(time.mktime(datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day-7).timetuple()))
        lst_last = datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day-1)
        ts_last = int(time.mktime(lst_last.timetuple()))
 
        itemid = self.__getItemid(hostid, itemname)
 
        function = getattr(self,'get%sValue' % table.capitalize())
 
        return  function(type,itemid, ts_first, ts_last)
 
    def getInfo(self):
        #循环读取IP列表信息
        for ip,resultdict in  zabbix.IpInfoList.items():
            print "正在查询 IP:%-15s hostid:%5d 的信息！" % (ip, resultdict['hostid'])
            #循环读取keys，逐个key统计数据：
            for value in keys:
                print "\t正在统计 key_:%s" % value[2]
                if not value[2] in zabbix.IpInfoList[ip]:
                    zabbix.IpInfoList[ip][value[2]] = {}
                data =  zabbix.getLastMonthData(value[3], resultdict['hostid'],value[1],value[2])
                zabbix.IpInfoList[ip][value[2]][value[3]] = data
 
 
    def writeToXls2(self):
        '''生成xls文件'''
        try:
            import xlsxwriter
 
            #创建文件
            workbook = xlsxwriter.Workbook(xlsfilename)
 
            #创建工作薄
            worksheet = workbook.add_worksheet()
 
            #写入第一列：
            worksheet.write(0,0,"主机".decode('utf-8'))
            i = 1
            for ip in self.IpInfoList:
                worksheet.write(i,0,ip)
                i = i + 1
 
            #写入其他列：
            i = 1
            for value in keys:
                worksheet.write(0,i,value[0].decode('utf-8'))
 
                #写入该列内容：
                j = 1
                for ip,result in self.IpInfoList.items():
                    if value[4]:
                        worksheet.write(j,i, value[4] % result[value[2]][value[3]])
                    else:
                        worksheet.write(j,i, result[value[2]][value[3]] / value[5])
                    j = j + 1
 
                i = i + 1
        except Exception,e:
            print e
 
 
 
    def __del__(self):
        '''关闭数据库连接'''
        self.cursor.close()
        self.conn.close()
 
if __name__ == "__main__":
    zabbix = ReportForm()
    zabbix.getInfo()
    zabbix.writeToXls2()
