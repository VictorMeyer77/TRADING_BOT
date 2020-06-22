from datetime import datetime


class Signal:

    def __init__(self, dfToPred, newsFormater, logger, models, symbolesDf, conf, predictionCol):

        self.dfToPred = dfToPred
        self.newsFormater = newsFormater
        self.logger = logger
        self.symbolesDf = symbolesDf
        self.models = models
        self.conf = conf
        self.col = predictionCol

    def insertPrediction(self, symbole, trend):

        try:
            self.col.insert_one({"symbole": symbole,
                                 "trend": str(trend),
                                 "period": self.conf["userParam"]["model"]["nbDayBeforePred"],
                                 "datePred": int(datetime.now().timestamp())})
        except Exception as e:
            self.logger.addLog("ERROR", "Signal", e)

    def run(self):

        if self.dfToPred is None:
            self.logger.addLog("WARNING", "Signal", "Aucune news à prédire")
        else:

            for index in self.dfToPred.index:

                symbolesDf = self.symbolesDf[self.symbolesDf["nom"].str.upper() == self.dfToPred.at[index, "entreprise"].upper()]
                id = symbolesDf.at[symbolesDf.index[0], "mt_id"]
                newsToPred = self.newsFormater.getDataToPredict(self.dfToPred[self.dfToPred.index == index])
                pred = self.models.getPredictions(self.models.model[0], self.models.model[1], newsToPred)
                self.logger.addLog("INFO", "Signal", "Prédiction {} pour {}".format(str(pred[0]), str(id)))
                self.insertPrediction(str(id), pred[0])