
# ----    CETTE CLASSE INSERE LES INFORMATIONS D'UN TRADE ---- #

class TradeInfo:

    def __init__(self, col, symbole, type, status, swap, comission, priceCurrent, priceOpen, profit, stoploss, takeprofit, dateMaj):

        self.col = col
        self.symbole = symbole
        self.type = type
        self.status = status
        self.swap = swap
        self.comission = comission
        self.priceCurrent = priceCurrent
        self.priceOpen = priceOpen
        self.profit = profit
        self.stoploss = stoploss
        self.takeprofit = takeprofit
        self.dateMaj = dateMaj

    def insert(self):

        try:
            self.col.insert({"symbole": self.symbole.replace("!", "#"),
                             "type": self.type,
                             "status": self.status,
                             "swap": self.swap,
                             "comission": self.comission,
                             "priceCurrent": self.priceCurrent,
                             "priceOpen": self.priceOpen,
                             "profit": self.profit,
                             "stoploss": self.stoploss,
                             "takeprofit": self.takeprofit,
                             "dateMaj": self.dateMaj})

        except Exception as e:
            print(e)