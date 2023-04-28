# -*- coding: UTF-8 -*- 

import json
class Result:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    errlevel = 0
    SQL = ''
    errormessage = ''
    Affected_rows = 0
    execute_time = ''
    stagestatus = ''

class ProgressResult:
    def dump(self):
        json_string = '[]'
        if self.fin_messages:
            json_string = json.dumps([ob.__dict__ for ob in self.finalMessages])
            self.finalMessages.clear()
        final_string = "{\"status\""+":"+str(self.status)+","+"\"messages\""+":"+str("\""+self.messages+"\"")+","+"\"finalMessages\""+":"+str(json_string)+"}"
        return final_string

    status = 0
    messages = 'None'
    fin_messages = []

