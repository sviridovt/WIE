import json


class JSONDatabase():

    def __init__(self, path):
        try:
            fl = open(path)
            self.path = path
            self.data = json.load(fl)
        except FileNotFoundError:
            fl = open(path, 'w+')
            self.data = []
        except json.JSONDecodeError:
            self.data = []
        fl.close()

    def __getattr__(self, name):
        return self.data[name]

    def save(self):
        with open(self.path, 'w+') as fl:
            jdata = self.data
            json.dump(jdata, fl)