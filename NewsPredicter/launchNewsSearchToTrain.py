from lib.newsDao import NewsDao
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
newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"],
                  symbolesDao, logger)
newsDao.getNews()