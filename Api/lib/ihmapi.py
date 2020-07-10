from bson.json_util import dumps

class Ihmapi:

    def __init__(self, client):

        self.client = client

    def getCol(self, collectionName):

        db = self.client[collectionName]
        return db[collectionName]

    @staticmethod
    def getObjects(col, filterColumn, filter):

        mongoRes = col.find({filterColumn: filter}) if (filter is not None and filterColumn is not None) else col.find()
        objects = {"objects": [doc for doc in mongoRes], "count": mongoRes.count()}

        return dumps(objects)

    def get(self, collectionName, filterColumn, filter):

        try:
            col = self.getCol(collectionName)
            return str(self.getObjects(col, filterColumn, filter))

        except Exception as e:
            print(e)
            return "Colonne inconnue ou filtre invalide"
