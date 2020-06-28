
# ----    CETTE CLASSE RETOURNE LES PARAMETRES DE TRADING ---- #

class TradeParameter:

    def __init__(self, col):

        self.col = col

    def getTradeParam(self):

        try:
            for conf in self.col.find({}).sort([("dateMaj", -1)]).limit(1):
                return conf["trade"]
        except Exception as e:
            print(e)
            return "ERROR"

    def get(self):

        conf = self.getTradeParam()
        if conf == "ERROR":
            return "ERROR"
        else:
            return "{0},{1},{2}".format(conf["stoploss"], conf["takeprofit"], conf["moneyByTrade"])