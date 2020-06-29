import json
from datetime import datetime

class Configuration:

    def __init__(self, col):

        self.col = col

    def insert(self, conf):

        try:
            confDict = json.loads(conf)
            confDict["dateMaj"] = int(datetime.now().timestamp())
            self.col.insert(confDict)
            return "1"

        except Exception as e:
            print(e)
            return "0"


