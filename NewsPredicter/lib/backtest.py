import pandas as pd
import matplotlib.pyplot as plt


# ----   CETTE CLASSE SIMULE UN TRADING POUR TESTER UN MODÈLE ---- #


class Backtest:

    def __init__(self, newsFormater, prices):

        self.newsFormater = newsFormater
        self.prices = prices

        self.model = None
        self.modelType = ""
        self.deposit = 0
        self.investPerTrade = 0
        self.stopLoss = 0
        self.takeProfit = 0
        self.history = {"date": [], "gain": []}

    # initialise les paramètres du backtest

    def setParam(self, model, modelType, deposit, investPerTrade, stopLoss=5, takeProfit=5):

        self.model = model
        self.modelType = modelType
        self.deposit = deposit
        self.investPerTrade = investPerTrade
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.history = {"date": [], "gain": []}

    # simule un pari boursier

    def trade(self, news, order):

        prices = self.prices[self.prices["date"] >= news.at[news.index[0], "publishedAt"]]
        prices = prices[prices["entreprise"] == news.at[news.index[0], "entreprise"]]

        if prices.shape[0] < 1:
            print("News too recent to predict")
            return -1
        priceOfTrade = prices.at[prices.index[0], "open"]
        balance = self.deposit

        # verification fond
        if balance < priceOfTrade:
            print("No enought money")
            return -1
        elif self.investPerTrade < priceOfTrade:
            print("Share too expensive to buy")
            return -1
        else:
            volume = self.investPerTrade // priceOfTrade

        # buy
        if order == 1:

            print("{0} {1} BUY {2} at {3}".format(prices.at[prices.index[0], "date"],
                                                  prices.at[prices.index[0], "entreprise"].upper(),
                                                  str(volume), str(priceOfTrade)))

            balance -= (priceOfTrade * volume)
            i = prices.index[0] + 1
            sell = False
            while i < prices.index[-1] and not sell:

                pxDate = prices.at[i, "date"]
                pxEnt = prices.at[i, "entreprise"].upper()

                if priceOfTrade * (1 - self.stopLoss / 100) > prices.at[i, "close"]:
                    balance += (prices.at[i, "close"] * volume)
                    print(
                        "{0} {1} STOPLOSS RESULT {2}".format(pxDate, pxEnt,
                                                             str((prices.at[i, "close"] - priceOfTrade) * volume)))
                    self.history["date"].append(pxDate)
                    self.history["gain"].append((prices.at[i, "close"] - priceOfTrade) * volume)
                    sell = True

                elif priceOfTrade * (1 + self.takeProfit / 100) < prices.at[i, "close"]:
                    balance += (prices.at[i, "close"] * volume)
                    print("{0} {1} TAKEPROFIT. RESULT {2}".format(pxDate, pxEnt,
                                                                  str((prices.at[i, "close"] - priceOfTrade) * volume)))
                    self.history["date"].append(pxDate)
                    self.history["gain"].append((prices.at[i, "close"] - priceOfTrade) * volume)
                    sell = True

                i += 1

        # sell
        elif order == 2:

            print("{0} {1} SELL {2} at {3}".format(prices.at[prices.index[0], "date"],
                                                   prices.at[prices.index[0], "entreprise"].upper(),
                                                   volume, str(priceOfTrade)))

            balance -= (priceOfTrade * volume)
            i = prices.index[0] + 1
            sell = False

            while i < prices.index[-1] and not sell:

                pxDate = prices.at[i, "date"]
                pxEnt = prices.at[i, "entreprise"]

                if priceOfTrade * (1 + self.stopLoss / 100) < prices.at[i, "close"]:
                    balance += (prices.at[i, "close"] * volume)
                    print("{0} {1} STOPLOSS. RESULT {2}".format(pxDate,
                                                                pxEnt,
                                                                str((priceOfTrade - prices.at[i, "close"]) * volume)))
                    self.history["date"].append(pxDate)
                    self.history["gain"].append((priceOfTrade - prices.at[i, "close"]) * volume)
                    sell = True

                elif priceOfTrade * (1 - self.takeProfit / 100) > prices.at[i, "close"]:
                    balance += (prices.at[i, "close"] * volume)
                    print("{0} {1} TAKEPROFIT. RESULT {2}".format(pxDate,
                                                                  pxEnt,
                                                                  str((priceOfTrade - prices.at[i, "close"]) * volume)))
                    self.history["date"].append(pxDate)
                    self.history["gain"].append((priceOfTrade - prices.at[i, "close"]) * volume)
                    sell = True

                i += 1
        return 0

    # projette un graphique de la simulation

    def plotResult(self):

        histDf = pd.DataFrame(self.history)
        histDf = histDf.sort_values("date")

        for i in range(0, len(histDf.index)):

            if i == 0:
                histDf.at[histDf.index[i], "gain"] = histDf.at[histDf.index[i], "gain"] + self.deposit

            else:
                histDf.at[histDf.index[i], "gain"] = histDf.at[histDf.index[i], "gain"] + histDf.at[histDf.index[i - 1],
                                                                                                    "gain"]

        histDf.set_index("date").plot()
        plt.xlabel("date")
        plt.ylabel("euros €")
        plt.legend()
        plt.title("Backtest")
        plt.show()

    # éxécute le backtest

    def run(self, newsToTest):

        newsToTest["publishedAt"] = pd.to_datetime(newsToTest["publishedAt"])
        newsToTest = self.newsFormater.roundTime(newsToTest, "publishedAt")
        newsToTest = newsToTest.reset_index(drop=True)

        newsToPred = self.newsFormater.getDataToPredict(newsToTest)

        for i in range(0, newsToPred.shape[0]):

            prediction = 0

            if self.modelType == "sklearn":
                prediction = self.model.predict([newsToPred[i]])[0]
            elif self.modelType == "keras":
                prediction = self.model.predict([newsToPred[i].tolist()]).argmax()

            if prediction != 0:
                self.trade(newsToTest[newsToTest.index == i], prediction)

        self.plotResult()
