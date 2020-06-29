# ----    SERVEUR POUR LA COMMUNICATION ENTRE L'ORACLE ET LE BOT ---- #

import cherrypy
import json
from lib.oracle import Oracle
from lib.accountInfo import AccountInfo
from lib.tradeInfo import TradeInfo
from lib.mongo import Mongo
from lib.tradeParameter import TradeParameter
from lib.configuration import Configuration
from lib.symbole import Symbole
from lib.ihmapi import Ihmapi


class Main(object):

    def __init__(self):
        self.conf = json.load(open("/conf/configuration.json", "r"))
        self.mongo = Mongo(self.conf["mongo"])

    @cherrypy.expose
    def index(self):
        return "TRADING BOT 4IABD API"

    @cherrypy.expose
    def oracle(self, flag):
        return Oracle(self.mongo.predictionCol, flag).getCsvPredictions()

    @cherrypy.expose
    def insertAccountInfo(self, currency, name, tradeMode, login, company, leverage, balance, equity, profit, dateMaj):
        return AccountInfo(self.mongo.accountInfoCol, currency, name, tradeMode, login, company, leverage, balance,
                           equity, profit, dateMaj).insert()

    @cherrypy.expose
    def insertTradeInfo(self, symbole, type, status, swap, comission, priceCurrent, priceOpen, profit, stoploss,
                        takeprofit, dateMaj):
        return TradeInfo(self.mongo.tradeInfoCol, symbole, type, status, swap, comission, priceCurrent, priceOpen,
                         profit, stoploss, takeprofit, dateMaj).insert()

    @cherrypy.expose
    def getTradeParameter(self):
        return TradeParameter(self.mongo.configurationCol).get()

    @cherrypy.expose
    def insertConfiguration(self, conf):
        return Configuration(self.mongo.configurationCol).insert(conf)

    @cherrypy.expose
    def updateSymbole(self, symbole):
        return Symbole(self.mongo.symbolesCol).update(symbole)

    @cherrypy.expose
    def ihmapi(self, collectionName, filterColumn=None, filter=None):
        return Ihmapi(self.mongo.client).get(collectionName, filterColumn, filter)


cherrypy.quickstart(Main(), config="/conf/server.conf")
