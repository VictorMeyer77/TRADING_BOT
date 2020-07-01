from lib.pricesDao import PricesDao
from lib.newsFormater import NewsFormater
from lib.backtest import Backtest
from lib.newsDao import NewsDao
from lib.models import Models
from lib.mongo import Mongo
from lib.symbolesDao import SymbolesDao
from lib.logger import Logger
from lib.configuration import Configuration


# ---- ÉXÉCUTE UN BACKTEST ---- #
# ---- lancer le docker-compose pour créer la base mongo db ---- #

if __name__ == "__main__":
    
    configuration = Configuration()
    logger = Logger(configuration.getConf()["logDirPath"])
    mongo = Mongo(configuration.getConf()["mongo"])
    configuration.setCollection(mongo.configurationCol)
    conf = configuration.getConf()

    symbolesDao = SymbolesDao(mongo.symbolesCol, conf["initSymbolJsonPath"], logger)
    symbolesDao.hydrateInitSymboles()
    symboles = symbolesDao.getSymboles()

    pricesDao = PricesDao(symboles, logger)

    newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"],
                      symbolesDao, logger)
    newsDao.hydrateInitNews()

    pricesDao.setPriceDf(60)
    #à décommenter pour ne pas avoir à récuperer les prix à chaque exécution
    pricesDao.writePrices(conf["pricesPath"])
    #pricesDao.loadPrices(conf["pricesPath"])

    newsFormater = NewsFormater(symboles, newsDao.getDfToTrain(), pricesDao.prices,
                                conf["userParam"]["model"]["nbDayBeforePred"],
                                conf["userParam"]["model"]["deltaToTrade"], logger)

    # au vue de notre faible quantité de données
    # il n'y a pas encore de données de validation
    x, y = newsFormater.getTrainingData()

    models = Models(x, y, x, y, mongo.modelCol, conf["userParam"]["model"], logger, conf["modelDir"])
    models.run()
    models.loadModel()
    model = models.model

    backest = Backtest(newsFormater, pricesDao.prices)
    newsToTest = newsDao.getDfToTrain()
    backest.setParam(model[0], model[1], 10000, 500, conf["userParam"]["trade"]["stoploss"], conf["userParam"]["trade"]["takeprofit"])
    backest.run(newsToTest)
