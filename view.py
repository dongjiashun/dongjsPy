from django.http import HttpResponse
import MySQLdb
 
def hello(request):
    conn = MySQLdb.connect(host='192.168.203.129',user='root',passwd='',db='',port=6669)
    print 1
    return HttpResponse("Hello world ! ")

def calc(request):
    a = 1
    b = 2
    c = 3
    print a,b,c
    m = a+b+c
    return HttpResponse(str(m))