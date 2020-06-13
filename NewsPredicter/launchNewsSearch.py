from lib.newsDao import NewsDao
from lib.mongo import Mongo
from lib.symbolesDao import SymbolesDao
from lib.logger import Logger
import json

conf = json.load(open("conf/configuration.json", "r"))
mongo = Mongo(conf["mongo"])
logger = Logger(conf["logDirPath"])
symbolesDao = SymbolesDao(mongo.symbolesCol, conf["initSymbolJsonPath"], logger)
symboles = symbolesDao.getSymboles()
newsDao = NewsDao(mongo.newsCol, mongo.newsColToPredCol, conf["newsKeyApi"],
                  symbolesDao, conf["initNewsDirPath"], logger)
newsDao.getNews()