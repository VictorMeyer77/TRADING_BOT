
# ----    CETTE CLASSE RETOURNE LES PRÉDICTIONS ---- #

class Oracle:

    def __init__(self, predictionsCol, flag):

        self.col = predictionsCol
        self.flag = flag

    def getJsonPredictions(self):

        try:
            return self.col.find({"datePred": {"$gte": int(self.flag)}}).sort([("datePred", 1)])
        except Exception as e:
            print(e)
            return "ERROR"

    def getCsvPredictions(self):

        answer = ""
        for pred in self.getJsonPredictions():
            answer += "{0},{1},{2},{3};".format(pred["symbole"], pred["trend"], pred["period"], pred["datePred"])

        return answer
