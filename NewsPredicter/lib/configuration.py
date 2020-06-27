import json

# --- Gère l'initialisation et la mise à jour de la configuration --- #

class Configuration:

    def __init__(self):

        self.conf = json.load(open("/conf/configuration.json", "r"))
        self.col = None

    def setCollection(self, collection):
        self.col = collection

    def getLastUserConf(self):

        try:
            for conf in self.col.find({}).sort([("date_maj", -1)]):
                return conf
        except Exception as e:
            return None

    def getConf(self):

        newConf = self.getLastUserConf()
        if newConf is not None:
            self.conf["userParam"] = newConf["userParam"]
        return self.conf
