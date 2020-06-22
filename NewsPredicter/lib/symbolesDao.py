import json
import pandas as pd


# ----    CETTE CLASSE GÈRE LA BASE DES SYMBOLES À TRAITER  ---- #


class SymbolesDao:

    def __init__(self, symbolesCol, initSymbolesJsonPath, logger):

        self.collection = symbolesCol
        self.initSymbolesJsonPath = initSymbolesJsonPath
        self.logger = logger
        self.symboles = None

    # init de la base de symbole

    def hydrateInitSymboles(self):

        self.logger.addLog("INFO", "SymbolesDao", "Initialistaion des symboles avec valeurs EURONEXT FR")
        symboles = json.load(open(self.initSymbolesJsonPath, "r", encoding="utf-8"))

        for symbole in symboles["symboles"]:

            try:
                if not self.testIfExist(symbole):
                    self.collection.insert_one(symbole)
            except Exception as e:
                self.logger.addLog("ERROR", "SymbolesDao",
                                   "Failed to insert symboles: {0} \n {1}".format(str(symbole), e))

    # retourne les symboles enregistrés

    def getSymboles(self):

        symbolesJson = self.collection.find({})
        symboles = {"indice": [], "mt_id": [], "nom": [], "supersecteur": [], "secteur": [], "pays": [], "flag": [], "actif": []}

        for symbole in symbolesJson:
            symboles["indice"].append(symbole["_id"])
            symboles["mt_id"].append(symbole["mt_id"])
            symboles["nom"].append(symbole["nom"])
            symboles["supersecteur"].append(symbole["supersecteur"])
            symboles["secteur"].append(symbole["secteur"])
            symboles["pays"].append(symbole["pays"])
            symboles["flag"].append(symbole["flag"])
            symboles["actif"].append(int(symbole["actif"]))

        self.logger.addLog("INFO", "SymbolesDao", "{} symboles à traités".format(str(len(symboles["indice"]))))
        return pd.DataFrame(symboles)

    # retourne les symboles actifs

    def getActivSymboles(self):

        symboles = self.getSymboles()
        return symboles[symboles["actif"] == 1]

    # test si le symbole existe

    def testIfExist(self, symbole):

        if self.collection.find_one({"_id": symbole["_id"]}) is not None:
            return True
        else:
            return False

    # met à jour le flag d'une entreprise

    def updateFlag(self, symboleName, date):

        currentSymbole = self.collection.find({"nom": symboleName.lower()})[0]
        updateSymbole = dict(currentSymbole)
        updateSymbole["flag"] = date
        self.collection.update_one(currentSymbole, {"$set": updateSymbole})
        self.logger.addLog("INFO", "SymbolesDao", "Flag de {0} modifié --> {1}".format(symboleName, str(date)))

    # récupère le flag d'une entreprise

    def getFlag(self, symboleName):

        symbole = self.collection.find({"nom": symboleName.upper()})[0]
        return symbole["flag"]
