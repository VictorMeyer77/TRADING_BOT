import pandas as pd
import nltk
import numpy as np


# ----    CETTE CLASSE FORMATE LES NEWS POUR LES ENTRAINEMENTS ET LES PRÉDICTIONS   ---- #


class NewsFormater:

    def __init__(self, symboles, news, prices, nbDayToPred, deltaToPred, logger):

        self.symboles = symboles
        self.prices = prices
        self.news = news
        self.logger = logger
        self.nbDayToPred = nbDayToPred
        self.deltaToPred = deltaToPred
        self.clearDataset = self.getClearDataset()
        self.keywords = self.getUsefullWords(self.getAllWords(self.clearDataset))

    # premier formatage des colonnes du dataset

    @staticmethod
    def formatCol(news):

        indexs, entreprise, datePub, text, imgUrl = [], [], [], [], []

        for index in news.index:

            indexs.append(index)
            entreprise.append(news.at[index, "entreprise"])
            datePub.append(news.at[index, "publishedAt"])
            imgUrl.append(news.at[index, "urlToImage"])

            # regroupement texte
            txt = news.at[index, "title"] + " " + news.at[index, "description"]
            if news.at[index, "content"] is not None:
                txt += news.at[index, "content"]
            text.append(" ".join(txt.split(" ")[:-3]).lower())

        df = pd.DataFrame({"index": indexs, "entreprise": entreprise,
                           "date_pub": datePub, "text": text, "img_url": imgUrl})
        df["date_pub"] = pd.to_datetime(df["date_pub"])

        return df

    # arrondit les heures au jour près

    @staticmethod
    def roundTime(news, dateColName):

        for index in news.index:
            roundTime = news.at[index, dateColName].timestamp() - news.at[index, dateColName].timestamp() % (
                    24 * 60 * 60)
            news.at[index, dateColName] = pd.to_datetime(int(roundTime), unit="s")

        return news

    # récupère tous les mots du dataset

    @staticmethod
    def getAllWords(news):

        words = []

        for txt in news.text:

            for w in txt.split(" "):
                words.append(w)

        return words

    # supprime ponctuation

    @staticmethod
    def tokenizeText(news):

        tokNews = news

        for index in tokNews.index:
            tokenizer = nltk.RegexpTokenizer(r'\w+')
            words = tokenizer.tokenize(tokNews.at[index, "text"])
            tokNews.at[index, "text"] = " ".join(words)

        return tokNews

    # retourne la liste de mots distincts classés par ordre croissant

    @staticmethod
    def getDistinctOrderWords(words):

        countWords = pd.DataFrame({"words": words, "ct": [1] * len(words)}).groupby(['words'])[
            "ct"].count().sort_values()
        return countWords

    # retourne les stopwords français

    def getStopwords(self, words):

        nltk.download('stopwords')
        sw = set()
        entNames = " ".join(self.symboles["nom"].to_list()).lower()
        sw.update(entNames.split(" "))
        sw.update(self.getDistinctOrderWords(words).to_list()[-50:])
        sw.update(tuple(nltk.corpus.stopwords.words('french')))
        self.logger.addLog("INFO", "NewsPredicter", "Stopwords: {} mots".format(str(len(sw))))

        return sw

    # supprime les articles dont le nom de l'entreprise n'apparit pas dans le contenu

    def removeNonPerti(self, news):

        clean_news = news
        banInd = []

        for index in clean_news.index:

            if clean_news.at[index, "entreprise"] not in clean_news.at[index, "text"].split(" "):
                banInd.append(index)

        self.logger.addLog("INFO", "NewsPredicter", "Supression de {} non pertinentes".format(str(len(banInd))))
        return clean_news.drop(banInd, axis=0)

    # retourne les mots importants des news pour formée les colonnes du dataset

    def getUsefullWords(self, words):

        distWord = self.getDistinctOrderWords(words).index.to_list()
        sw = self.getStopwords(words)

        i = 0
        while i < len(distWord):

            w = str(distWord[i])
            if w in sw:
                del distWord[i]
                i -= 1
            i += 1

        return distWord

    # joint les prix au news

    def joinNewsPrices(self, news, prices):

        priceNews = news
        priceNews["trend"] = 0
        banInd = []

        for index in priceNews.index:

            tmp = prices[prices["entreprise"] == priceNews.at[index, "entreprise"]]
            tmp = tmp[tmp["date"] == priceNews.at[index, "date_pub"]]

            if tmp.shape[0] == 0 or \
                    tmp.index + self.nbDayToPred > prices.shape[0] or \
                    prices.at[tmp.index[0], "entreprise"] != prices.at[(tmp.index + self.nbDayToPred)[0], "entreprise"]:
                banInd.append(index)

            else:
                start = prices.at[tmp.index[0], "open"]
                end = prices.at[(tmp.index + self.nbDayToPred)[0], "close"]

                if (end - start) / start > self.deltaToPred / 100:
                    priceNews.at[index, "trend"] = 1
                elif (end - start) / start < -(self.deltaToPred / 100):
                    priceNews.at[index, "trend"] = 2
                else:
                    priceNews.at[index, "trend"] = 0

        self.logger.addLog("INFO", "NewsPredicter", "Concaténation des prix n+{} après la news".format(self.nbDayToPred))
        return priceNews.drop(banInd, axis=0)

    # applique les fonctions pour créer le dataset

    def getClearDataset(self):

        self.logger.addLog("INFO", "NewsFormater",
                           "Démarrage création dataset: {} lignes".format(str(self.news.shape[0])))
        news = self.formatCol(self.news)
        news = self.roundTime(news, "date_pub")
        news = self.removeNonPerti(news)
        news = self.tokenizeText(news)
        return self.joinNewsPrices(news, self.prices)

    # créer le dataset d'entrainement

    def getTrainingData(self):

        xTrain, yTrain = {}, []

        for word in self.keywords:
            xTrain[word] = [0] * self.clearDataset.shape[0]
        xTrain = pd.DataFrame(xTrain)

        index = 0

        for ind in self.clearDataset.index:

            for w in self.clearDataset.at[ind, "text"]:

                if w in xTrain.columns.to_list():
                    xTrain.at[index, w] = 1

            index += 1
            yTrain.append(self.clearDataset.at[ind, "trend"])

        self.logger.addLog("INFO", "NewsPredicter",
                           "Génération des données d'entrainement. x_train shape: {}".format(str(xTrain.shape)))
        return xTrain.to_numpy(), np.array(yTrain)

    # retourne news formatées pour la prédiction

    def getDataToPredict(self, newsToPred):

        news = self.formatCol(newsToPred)
        news = self.roundTime(news, "date_pub")
        maj_news = self.removeNonPerti(news)
        news = self.tokenizeText(news)
        news = news.reset_index(drop=True)

        xTest = {}
        for word in self.keywords:
            xTest[word] = [0] * newsToPred.shape[0]
        xTest = pd.DataFrame(xTest)

        for i in range(0, newsToPred.shape[0]):

            if newsToPred.index[i] not in maj_news.index:
                continue

            for word in " ".join(news.at[i, "text"]):

                if word in xTest.columns.to_list():
                    xTest.at[i, word] = 1

        self.logger.addLog("INFO", "NewsPredicter",
                           "Génération des données à tester. x_test shape: {}".format(str(xTest.shape)))
        return xTest.to_numpy()
