from lib.pricesDao import PricesDao
from lib.newsFormater import NewsFormater
from lib.newsDao import NewsDao
from lib.models import Models
from lib.mongo import Mongo
from lib.symbolesDao import SymbolesDao
from lib.logger import Logger
import json


conf = json.load(open("conf/configuration.json", "r"))
mongo = Mongo(conf["mongo"])
logger = Logger(conf["logDirPath"])
symbolesDao = SymbolesDao(mongo.symbolesCol, conf["initSymbolJsonPath"], logger)
symboles = symbolesDao.getSymboles()
pricesDao = PricesDao(symboles, logger)
pricesDao.loadPrices(conf["pricesPath"])
newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"], symbolesDao, conf["initNewsDirPath"], logger)
newsFormater = NewsFormater(symboles, newsDao.getDfToTrain(), pricesDao.prices,
                            conf["model"]["nbDayBeforePred"], conf["model"]["deltaToTrade"], logger)
x, y = newsFormater.getTrainingData()
models = Models(x, y, x, y, mongo.modelCol, conf["model"], logger)
models.run()