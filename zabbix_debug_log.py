import requests
import json

headers = {
    'Content-Type': 'application/json'
}

class GetZabbix:
    def __init__(self):
        self.username = "22216"
        self.password = "1212Ming"
        self.url = "http://10.33.119.29/zabbix/api_jsonrpc.php"
        self.token = self.getToken()

    def getToken(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 2,
            "auth": None
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        token = json.loads(r.content).get("result")
        return token

    def getHosts(self):
        data = {
               "jsonrpc": "2.0",
                "method": "alert.get",
                "params": {
                    "output": "extend",
                    "groupids": "10"
                },
            "id": 2,
            "auth": self.token
        }
        r = requests.post(url=self.url, headers=headers, data=json.dumps(data))
        print(r.content)


if __name__ == "__main__":
    start = GetZabbix()
    start.getHosts()