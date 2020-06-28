from pymongo import MongoClient


# ----    CETTE CLASSE REPERTORIE LES COLLECTIONS MONGO DB ---- #


class Mongo:

    def __init__(self, mongoConf):
        client = MongoClient(mongoConf["host"], mongoConf["port"])

        predictionDb = client[mongoConf["predictionName"]]
        self.predictionCol = predictionDb[mongoConf["predictionName"]]

        accountInfoDb = client[mongoConf["accountInfoName"]]
        self.accountInfoCol = accountInfoDb[mongoConf["accountInfoName"]]

        tradeInfoDb = client[mongoConf["tradeInfoName"]]
        self.tradeInfoCol = tradeInfoDb[mongoConf["tradeInfoName"]]

        configurationDb = client[mongoConf["configurationName"]]
        self.configurationCol = configurationDb[mongoConf["configurationName"]]
