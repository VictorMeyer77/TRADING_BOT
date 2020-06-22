from pymongo import MongoClient


# ----    CETTE CLASSE REPERTORIE LES COLLECTIONS MONGO DB ---- #


class Mongo:

    def __init__(self, mongoConf):
        client = MongoClient(mongoConf["host"], mongoConf["port"])

        newsDb = client[mongoConf["newsName"]]
        self.newsCol = newsDb[mongoConf["newsName"]]

        newsToPredDb = client[mongoConf["newsToPredName"]]
        self.newsColToPredCol = newsToPredDb[mongoConf["newsToPredName"]]

        modelDb = client[mongoConf["modelName"]]
        self.modelCol = modelDb[mongoConf["modelName"]]

        symbolesDb = client[mongoConf["symbolName"]]
        self.symbolesCol = symbolesDb[mongoConf["symbolName"]]

        predictionDb = client[mongoConf["predictionName"]]
        self.predictionCol = predictionDb[mongoConf["predictionName"]]

        configurationDb = client[mongoConf["configurationName"]]
        self.configurationCol = configurationDb[mongoConf["configurationName"]]
