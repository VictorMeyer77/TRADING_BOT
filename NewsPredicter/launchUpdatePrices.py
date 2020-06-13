from lib.pricesDao import PricesDao
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
pricesDao.setPriceDf(365)
pricesDao.writePrices(conf["pricesPath"])


