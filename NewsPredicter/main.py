from lib.pricesDao import PricesDao
from lib.newsFormater import NewsFormater
from lib.backtest import Backtest
from lib.newsDao import NewsDao
from lib.models import Models
from lib.mongo import Mongo
from lib.symbolesDao import SymbolesDao
from lib.logger import Logger
import json


# ---- ÉXÉCUTE UN BACKTEST ---- #
# ---- lancer le docker-compose pour créer la base mongo db ---- #

if __name__ == "__main__":
    
    conf = json.load(open("conf/configuration.json", "r"))

    logger = Logger(conf["logDirPath"])

    mongo = Mongo(conf["mongo"])
    
    symbolesDao = SymbolesDao(mongo.symbolesCol, conf["initSymbolJsonPath"], logger)
    symbolesDao.hydrateInitSymboles()
    symboles = symbolesDao.getSymboles()

    pricesDao = PricesDao(symboles, logger)

    newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"],
                      symbolesDao, conf["initNewsDirPath"], logger)
    newsDao.hydrateInitNews()

    #pricesDao.setPriceDf(60)
    #à décommenter pour ne pas avoir à récuperer les prix à chaque exécution
    #pricesDao.writePrices(conf["pricesPath"])
    pricesDao.loadPrices(conf["pricesPath"])

    newsFormater = NewsFormater(symboles, newsDao.getDfToTrain(), pricesDao.prices,
                                conf["model"]["nbDayBeforePred"], conf["model"]["deltaToTrade"], logger)

    # au vue de notre faible quantité de données
    # il n'y a pas encore de données de validation
    x, y = newsFormater.getTrainingData()

    models = Models(x, y, x, y, mongo.modelCol, conf["model"], logger)
    models.run()
    models.loadModel()
    model = models.model

    backest = Backtest(newsFormater, pricesDao.prices)
    newsToTest = newsDao.getDfToTrain()
    backest.setParam(model[0], model[1], 10000, 500, conf["trade"]["stoploss"], conf["trade"]["takeprofit"])
    backest.run(newsToTest)
