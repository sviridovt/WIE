import json


class JSONDatabase():

    def __init__(self, path, name):
        fl = open(path)
        self.path = path
        self.data = json.load(fl)
        self.name = name
        fl.close()
        self.data = self.date[name]

    def __getattr__(self, name):
        return self.data[name]

    def save(self):
        fl = open(self.path, 'wr')
        jdata = json.load(fl)
        jdata[self.name] = self.data
        jdata.seek(0)
        json.dump(jdata, fl)
        jdata.truncate()