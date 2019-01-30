import json


class JSONDatabase():

    def __init__(self, path):
        fl = open(path)
        self.path = path
        self.data = json.load(fl)
        fl.close()

    def __getattr__(self, name):
        return self.data[name]

    def save(self):
        fl = open(self.path, 'wr')
        #jdata = json.load(fl)
        jdata = self.data
        jdata.seek(0)
        json.dump(jdata, fl)
        jdata.truncate()