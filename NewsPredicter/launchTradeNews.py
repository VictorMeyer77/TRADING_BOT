from lib.pricesDao import PricesDao
from lib.newsFormater import NewsFormater
from lib.newsDao import NewsDao
from lib.models import Models
from lib.mongo import Mongo
from lib.symbolesDao import SymbolesDao
from lib.logger import Logger
from lib.trader import Trader
import json

conf = json.load(open("conf/configuration.json", "r"))
logger = Logger(conf["logDirPath"])
mongo = Mongo(conf["mongo"])
symbolesDao = SymbolesDao(mongo.symbolesCol, conf["initSymbolJsonPath"], logger)
symbolesDao.hydrateInitSymboles()
symboles = symbolesDao.getSymboles()
pricesDao = PricesDao(symboles, logger)

newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"],
                  symbolesDao, conf["initNewsDirPath"], logger)

pricesDao.loadPrices(conf["pricesPath"])

newsFormater = NewsFormater(symboles, newsDao.getDfToTrain(), pricesDao.prices,
                            conf["model"]["nbDayBeforePred"], conf["model"]["deltaToTrade"], logger)


x, y = newsFormater.getTrainingData()
models = Models(x, y, x, y, mongo.modelCol, conf["model"], logger)
models.loadModel()

trader = Trader(newsDao.getDfToPred(), newsFormater, logger, models, symboles)
trader.run()
