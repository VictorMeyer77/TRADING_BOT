from newsapi import NewsApiClient
import json
import pandas as pd


# ----  CETTE CLASSE EST CHARGÉE DE RÉCUPÉRER ET RESTITUER LES NEWS ÉCONOMIQUES ---- #


class NewsDao:

    def __init__(self, newsCol, newsToPredCol, apiKey, symbolesDao, initNewsDirPth, logger):

        self.newsCol = newsCol
        self.newsToPredCol = newsToPredCol
        self.symbolesDao = symbolesDao
        self.initNewsDirPth = initNewsDirPth
        self.newsApi = NewsApiClient(api_key=apiKey)
        self.logger = logger

    # insert une news dans la base de news

    def insertNews(self, news):

        try:
            self.newsCol.insert_one(news)
            self.logger.addLog("INFO", "NewsDao", "Insertion news: {}".format(str(news)))
        except Exception as e:
            self.logger.addLog("ERROR", "NewsDao", "ailed to insert news: {} \n {}".format(str(news), e))

    # test si une news est déjà dans la base de news

    def isNewsExist(self, news):

        if self.newsCol.find_one({"_id": news["_id"]}) is not None:
            return True
        else:
            return False

    # insert une news dans la base de news de prediction

    def insertNewsToPred(self, news):

        try:
            self.newsToPredCol.insert_one(news)
            self.logger.addLog("INFO", "NewsDao", "Insertion newsToPred: {}".format(str(news)))
        except Exception as e:
            self.logger.addLog("ERROR", "NewsDao", "Failed to insert newsToPred: {} \n {}".format(str(news), e))

    # test si une news est déjà dans la base de news de prediction

    def isNewsToPredExist(self, news):

        if self.newsToPredCol.find_one({"_id": news["_id"]}) is not None:
            return True
        else:
            return False

    # retourne les news d'entrainement formatées

    def getDfToTrain(self):

        newsJson = self.newsCol.find({})
        newsDf = []

        for news in newsJson:
            newsDf.append(pd.DataFrame([news]))

        self.logger.addLog("INFO", "NewsDao", "Récupération news d'entrainement: {}".format(str(len(newsDf))))

        return pd.concat(newsDf, ignore_index=True).drop(["_id"], axis=1)

    # retourne les news à prédire formatées

    def getDfToPred(self):

        newsToPredJson = self.newsToPredCol.find({})
        newsToPredDf = []

        for news in newsToPredJson:
            newsToPredDf.append(pd.DataFrame([news]))

        self.transferNewsToPred()
        self.logger.addLog("INFO", "NewsDao", "Récupération news à prédire: {}".format(str(len(newsToPredDf))))

        if len(newsToPredDf) < 1:
            return None
        else:
            return pd.concat(newsToPredDf, ignore_index=True).drop(["_id"], axis=1)

    # transfert les news à prédire dans la base des news

    def transferNewsToPred(self):

        newsToPredJson = self.newsToPredCol.find({})

        for news in newsToPredJson:
            self.insertNews(news)

        self.newsToPredCol.delete_many({})
        self.logger.addLog("INFO", "NewsDao",
                           "Transfert de {} news à prédire dans la base de news".format(str(newsToPredJson.count())))

    # récupère et insere dans les bases les nouvelles news

    def getNews(self):

        self.logger.addLog("INFO", "NewsDao", "Récupération des nouvelles news")

        for nom in self.symbolesDao.getSymboles().nom:

            try:
                entNnews = self.newsApi.get_everything(q=nom.lower(),
                                                       sources="les-echos",
                                                       from_param=self.symbolesDao.getFlag(nom),
                                                       to=pd.to_datetime("today"))
            except Exception:
                entNnews = self.newsApi.get_everything(q=nom.lower(),
                                                       sources="les-echos")

            for art in entNnews["articles"]:

                art["entreprise"] = nom.lower()
                art["_id"] = self.hash(art)

                if not self.isNewsExist(art):

                    if self.isToPred(art):
                        if not self.isNewsToPredExist(art):
                            self.insertNewsToPred(art)
                            self.logger.addLog("INFO", "NewsDao", "Nouvelle news {} à prédire".format(nom.upper()))
                    else:
                        self.insertNews(art)
                        self.logger.addLog("INFO", "NewsDao", "Nouvelle news {} pour l'entrainement".format(nom.upper()))

    # ne sert qu'a l'initialisation pour charger un minimum de news

    def hydrateInitNews(self):

        self.logger.addLog("INFO", "NewsDao", "Initialisation des news")
        for sym in self.symbolesDao.getSymboles().nom:
            content = json.load(open("{0}/{1}.json".format(self.initNewsDirPth, sym.lower()), "r", encoding="utf-8"))

            for art in content["articles"]:

                art["entreprise"] = sym.lower()
                art["_id"] = self.hash(art)

                if not self.isNewsExist(art):
                    self.insertNews(art)

            # mise à jour du flag
            articleDf = pd.DataFrame(content["articles"])
            if articleDf.shape[0] > 0:
                lastArt = articleDf.sort_values(by=["publishedAt"], ascending=False)
                self.symbolesDao.updateFlag(lastArt.at[0, "entreprise"], pd.to_datetime(lastArt.at[0, "publishedAt"]))

    # test si la news à moins de 24h

    @staticmethod
    def isToPred(news):

        now = pd.to_datetime("today")
        newsDate = pd.to_datetime(news["publishedAt"])
        return now.timestamp() - 24 * 60 * 60 < newsDate.timestamp()

    # retourne un hash de la news pour l'unicité de la base
    # PYTHONHASHSEED=0
    @staticmethod
    def hash(news):

        return abs(hash(str(news["url"] + news["entreprise"]))) % (10 ** 8)
