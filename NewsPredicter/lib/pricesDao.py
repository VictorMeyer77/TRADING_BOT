import yfinance as yf
import pandas as pd

# ----    CETTE CLASSE RÉCUPÈRE ET RESTITUE LES PRIX DES VALEURS BOURSIÈRES  ---- #


class PricesDao:

    def __init__(self, symboles, logger):
        self.symboles = symboles
        self.prices = None
        self.logger = logger

    # récupération des prix

    def setPriceDf(self, nbDay):

        self.logger.addLog("INFO", "PricesDao", "Récupération des prix...")
        df = {"date": [], "entreprise": [], "open": [], "close": []}

        for symInd in self.symboles.index:
            prices = yf.Ticker(self.symboles.at[symInd, "indice"]).history(period="{0}d".format(str(nbDay)))

            for index in prices.index:
                df["date"].append(index)
                df["entreprise"].append(self.symboles.at[symInd, "nom"].lower())
                df["open"].append(prices.at[index, "Open"])
                df["close"].append(prices.at[index, "Close"])

        self.prices = pd.DataFrame(df)

    # écrit les prix dans un csv

    def writePrices(self, outputPath):

        self.prices.to_csv(outputPath)
        self.logger.addLog("INFO", "PricesDao", "Prix stockés dans {}".format(outputPath))

    # charge les prix du csv

    def loadPrices(self, outputPath):

        self.prices = pd.read_csv(outputPath, index_col=0)
        self.prices["date"] = pd.to_datetime(self.prices["date"])
        self.logger.addLog("INFO", "PicesDao",
                           "Chargement des prix {}: {} lignes".format(outputPath, self.prices.shape[0]))
