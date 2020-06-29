from pymongo import MongoClient


# ----    CETTE CLASSE REPERTORIE LES COLLECTIONS MONGO DB ---- #


class Mongo:

    def __init__(self, mongoConf):
        self.client = MongoClient(mongoConf["host"], mongoConf["port"])

        predictionDb = self.client[mongoConf["predictionName"]]
        self.predictionCol = predictionDb[mongoConf["predictionName"]]

        accountInfoDb = self.client[mongoConf["accountInfoName"]]
        self.accountInfoCol = accountInfoDb[mongoConf["accountInfoName"]]

        tradeInfoDb = self.client[mongoConf["tradeInfoName"]]
        self.tradeInfoCol = tradeInfoDb[mongoConf["tradeInfoName"]]

        configurationDb = self.client[mongoConf["configurationName"]]
        self.configurationCol = configurationDb[mongoConf["configurationName"]]
        
        symbolesDb = self.client[mongoConf["symbolesName"]]
        self.symbolesCol = symbolesDb[mongoConf["symbolesName"]]
