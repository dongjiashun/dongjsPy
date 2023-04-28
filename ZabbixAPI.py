import requests
import json

headers = {
    'Content-Type': 'application/json'
}

class GetZabbix:
    def __init__(self):
        #用户信息
        self.username = "22216"
        self.password = ""
        self.url = "http://192.168.0.*/zabbix/api_jsonrpc.php"
        self.token = self.getToken()

    def getToken(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 1,
            "auth": None
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        token = json.loads(r.content).get("result")
        return token

    def getHosts(self):
        data = {
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
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        print(r.content)


if __name__ == "__main__":
    start = GetZabbix()
    start.getHosts()