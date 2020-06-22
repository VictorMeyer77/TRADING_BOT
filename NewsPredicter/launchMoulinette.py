from lib.pricesDao import PricesDao
from lib.newsFormater import NewsFormater
from lib.newsDao import NewsDao
from lib.models import Models
from lib.mongo import Mongo
from lib.symbolesDao import SymbolesDao
from lib.logger import Logger
from lib.configuration import Configuration

configuration = Configuration()
logger = Logger(configuration.getConf()["logDirPath"])
mongo = Mongo(configuration.getConf()["mongo"])
configuration.setCollection(mongo.configurationCol)
conf = configuration.getConf()

symbolesDao = SymbolesDao(mongo.symbolesCol, conf["initSymbolJsonPath"], logger)
symboles = symbolesDao.getSymboles()
pricesDao = PricesDao(symboles, logger)
pricesDao.loadPrices(conf["pricesPath"])
newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"], symbolesDao, logger)
newsFormater = NewsFormater(symboles, newsDao.getDfToTrain(), pricesDao.prices,
                            conf["userParam"]["model"]["nbDayBeforePred"],
                            conf["userParam"]["model"]["deltaToTrade"], logger)
x, y = newsFormater.getTrainingData()
models = Models(x, y, x, y, mongo.modelCol, conf["userParam"]["model"], logger, conf["modelDir"])
models.run()