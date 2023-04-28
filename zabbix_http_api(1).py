#coding=utf-8
import requests
import json

class ZabbixAPI(object):
    def __init__(self):
        self.url = 'https://zabbix50.mistong.com/zabbix/api_jsonrpc.php'
        self.headers = {'Content-Type': 'application/json-rpc'}
        self.username = "mistongops"
        self.password = "mst@Qazwsx123"
        self.token = self.login()
    def login(self):
        params = {
                  "jsonrpc": "2.0",
                  "method": "user.login",
                  "params": {
                      "user": self.username,
                      "password": self.password
                  },
                  "id": 2,
                  "auth": None
              } 
        r = requests.post(self.url, data=json.dumps(params), headers=self.headers)
        token = json.loads(r.content).get("result")
        return token

    def get_hosts(self):
        params = {
                  "jsonrpc": "2.0",
                  "method": "host.get",
                  "params": {
                      "output": [
                          "hostid",
                          "host"
                      ],
                      "selectInterfaces": [
                          "interfaceid",
                          "ip"
                      ]
                  },
                  "id": 2,
                  "auth": self.token
              } 
        r = requests.get(self.url, data=json.dumps(params), headers=self.headers)
        print(r.text)
    
    def get_appinfo(self):
        params = {
            "jsonrpc": "2.0",
            "method": "apiinfo.version",
            "params": [],
            "id": 2
        }
        r = requests.get(self.url,data=json.dumps(params),headers=self.headers)
        print(r.text)
    def get_alert(self):
        params = {
            "jsonrpc": "2.0",
            "method": "alert.get",
            "params": {
                "output": ["alertid","clock","subject","message"],
                "groupids": "69",
                "time_from": "1566403200"
            },
                "id": 2,
                "auth": self.token  
        }
        response= requests.get(self.url,data=json.dumps(params),headers=self.headers)
        #print(response.text.decode('unicode_escape'))
        str=response.text.decode('unicode_escape')
 
        print str

    def get_history(self):
        params = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 3,
                "itemids": "558012",
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 1
            },
            "auth": self.token,
            "id": 2
        }
        r = requests.get(self.url,data=json.dumps(params),headers=self.headers)
        

if __name__ == "__main__":
    test = ZabbixAPI()
    #test.get_alert()
    test.login()
    #test.get_appinfo()
    #test.get_alert()
    #test.get_hosts()
