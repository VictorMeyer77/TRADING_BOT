import os
from datetime import datetime


class Logger:

    def __init__(self, logDir):

        self.logDir = logDir
        self.currentLogPath = logDir + "/" + datetime.now().strftime("%Y-%m-%d") + ".log"

        if not self.isLogFileExist():
            self.createLogFile()

    # génère le fichier de log
    def createLogFile(self):

        if not os.path.isfile(self.currentLogPath):
            file = open(self.currentLogPath, "w+")
            file.close()

    # récupère log
    def getLogContent(self):

        file = open(self.currentLogPath, "r")
        content = file.read()
        return content

    # ajoute un log
    def addLog(self, categorie, classe, content):

        file = open(self.currentLogPath, "a")
        message = "{0} [**{1}**] CLASSE {2} --> {3} \n".format(
            datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
            categorie.upper(),
            classe,
            content)

        print(message)
        file.write(message)
        file.close()

    # supprime les logs
    def truncateLogDir(self):

        for file in os.listdir(self.logDir):
            os.remove(self.logDir + "/" + file)

    # teste si le fichier de log existe
    def isLogFileExist(self):

        return os.path.exists(self.currentLogPath)
