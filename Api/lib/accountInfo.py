# ----    CETTE CLASSE INSÈRE LES INFORMATIONS DU COMPTE DE L'UTILISATEUR ---- #

class AccountInfo:

    def __init__(self, col, currency, name, tradeMode, login, company, leverage, balance, equity, profit, dateMaj):

        self.col = col
        self.currency = currency
        self.name = name
        self.tradeMode = tradeMode
        self.login = login
        self.company = company
        self.leverage = leverage
        self.balance = balance
        self.equity = equity
        self.profit = profit
        self.dateMaj = dateMaj

    def insert(self):

        try:
            self.col.insert({"currency": self.currency,
                             "name": self.name,
                             "tradeMode": self.tradeMode,
                             "login": self.login,
                             "company": self.company,
                             "leverage": self.leverage,
                             "balance": self.balance,
                             "equity": self.equity,
                             "profit": self.profit,
                             "dateMaj": self.dateMaj})
        except Exception as e:
            print(e)
