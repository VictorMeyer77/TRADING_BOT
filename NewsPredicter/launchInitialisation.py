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

configuration.initialize()
symbolesDao = SymbolesDao(mongo.symbolesCol, conf["initSymbolJsonPath"], logger)
symbolesDao.hydrateInitSymboles()
newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"], symbolesDao, logger)
newsDao.hydrateInitNews()