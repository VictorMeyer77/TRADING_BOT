import json
import datetime

# --- Gère l'initialisation et la mise à jour de la configuration --- #

class Configuration:

    def __init__(self):

        self.conf = json.load(open("conf/configuration.json", "r"))
        self.col = None

    def setCollection(self, collection):
        self.col = collection

    def getLastUserConf(self):

        try:
            for conf in self.col.find({}).sort([("dateMaj", -1)]).limit(1):
                return conf
        except Exception as e:
            return None

    def getConf(self):

        newConf = self.getLastUserConf()
        if newConf is not None:
            self.conf["userParam"] = newConf
        return self.conf

    def initialize(self):
        try:
            if self.col.find({}).count() == 0:
                configuration = self.conf["userParam"]
                configuration["dateMaj"] = int(datetime.datetime.now().timestamp())
                self.col.insert_one(configuration)
        except Exception as e:
            print(e)