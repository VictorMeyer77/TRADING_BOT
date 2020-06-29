import json


class Symbole:

    def __init__(self, col):

        self.col = col

    def isSymbolExist(self, symboleId):

        return self.col.find({"_id": symboleId}).count() > 0

    def updateActivity(self, activity, symboleId):

        self.col.update_one({"_id": symboleId}, {"$set": {"actif": activity}})

    def update(self, symbole):

        try:
            jsonSymbole = json.loads(symbole)
            if self.isSymbolExist(jsonSymbole["_id"]):
                self.updateActivity(jsonSymbole["actif"], jsonSymbole["_id"])
            else:
                self.col.insert(jsonSymbole)
            return "1"

        except Exception as e:
            print(e)
            return "0"
