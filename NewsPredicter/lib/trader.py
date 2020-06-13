class Trader:

    def __init__(self, dfToPred, newsFormater, logger, models, symbolesDf):

        self.dfToPred = dfToPred
        self.newsFormater = newsFormater
        self.logger = logger
        self.symbolesDf = symbolesDf
        self.models = models

    def run(self):

        if self.dfToPred is None:
            self.logger.addLog("WARNING", "Trader", "Aucune news à prédire")
        else:

            for index in self.dfToPred.index:

                symbolesDf = self.symbolesDf[self.symbolesDf["nom"].str.upper() == self.dfToPred.at[index, "entreprise"].upper()]
                indice = symbolesDf.at[symbolesDf.index[0], "indice"]
                newsToPred = self.newsFormater.getDataToPredict(self.dfToPred[self.dfToPred.index == index])
                pred = self.models.getPredictions(self.models.model[0], self.models.models.model[1], newsToPred)
                self.logger.addLog("INFO", "Trader", "Prédiction {} pour {}".format(str(pred), str(indice)))