from .. import settings
from .json import JSONDatabase


class Database():

    def __init__(self, params):
        if settings.DB_TYPE == 'json':
            self.db = JSONDatabase(settings.DB_FILE)
        else:
            raise ValueError(settings.DB_TYPE + " is not a valid database option, see documentation for help")

    def open(self, name):
        pass

    def save(self):
        self.db.save()