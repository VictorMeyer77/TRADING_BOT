from sklearn.svm import LinearSVC
from tensorflow.keras.layers import *
from tensorflow.keras.metrics import *
from tensorflow.keras.models import *
from tensorflow.keras.utils import *
from tensorflow.keras.models import load_model
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os
from joblib import dump, load
import shutil

# ---   CETTE CLASSE GÈRE ET TEST LES MODÈLES --- #


class Models:

    def __init__(self, xTrain, yTrain, xTest, yTest, modelCol, conf, logger, modelDir):

        self.modelCol = modelCol
        self.xTrain = xTrain
        self.yTrain = yTrain
        self.xTest = xTest
        self.yTest = yTest
        self.models = {}
        self.stats = None
        self.model = None
        self.conf = conf
        self.logger = logger
        self.modelDir = modelDir

    # SKLEARN

    # SVM

    def linearSvc(self):

        model = LinearSVC()
        model.fit(self.xTrain, self.yTrain)
        self.models["linearSVC"] = [model, "sklearn"]
        self.logger.addLog("INFO", "Models", "Fin entrainement du LinearSVC sklearn")

    # KERAS
    # MOULINETTE MLP

    # génère les patterns de modèle pour la moulinette

    def getPatternToTrain(self,  neuralPerLayer, layerActivation, nbOutput):

        patterns = {}
        outputLayer = []
        neurals = []

        for i in range(0, len(neuralPerLayer) + 1):
            if i == 0:
                for activation in layerActivation:
                    outputLayer.append([[nbOutput, activation]])
                    for nbNeural in neuralPerLayer:
                        neurals.append([nbNeural, activation])
                patterns[i] = outputLayer

            else:
                tmp = []
                for neural in neurals:
                    for mdl in patterns[i - 1]:
                        newPat = [neural] + mdl
                        tmp.append(newPat)
                patterns[i] = tmp

        self.logger.addLog("INFO", "Models", "Généraion des {} patterns MLP terminée".format(len(patterns)))
        return patterns

    # créer un modèle à partir d'un pattern
    @staticmethod
    def createModel(modelPattern, xShape):

        model = Sequential()
        model.add(Flatten(input_shape=xShape))
        for layer in modelPattern:
            model.add(Dense(layer[0], activation=layer[1]))

        model.compile(loss=categorical_crossentropy, metrics=[categorical_accuracy])
        return model

    # génère un MLP par pattern

    def generateMlp(self, modelPatterns, batchSize, epochs):

        for i in range(0, len(modelPatterns)):

            for pattern in modelPatterns[i]:
                model = self.createModel(pattern, self.xTrain[0].shape)
                model.summary()
                model.fit(self.xTrain, to_categorical(self.yTrain), epochs=epochs, batch_size=batchSize)
                self.models[str(pattern)] = [model, "keras"]

    # STATISTIQUES

    # retourne les prédictions d'un modèles
    @staticmethod
    def getPredictions(model, modelType, xTest):

        predictions = []
        for sample in xTest:
            if modelType == "keras":
                predictions.append(model.predict(np.array([sample])).argmax())
            elif modelType == "sklearn":
                predictions.append(model.predict([sample])[0])
        return predictions

    # retourne l'accuracy sur données de test d'un model

    def getAccuracy(self, predictions):

        nbGoodPred = 0
        i = 0

        for i in range(0, len(predictions)):

            if predictions[i] == self.yTest[i]:
                nbGoodPred += 1

        return round(nbGoodPred / len(predictions), 3)

    # retourne l'accuracy des trades d'un modèle

    def getTradeAccuracy(self, predictions):

        nbGoodPred = 0
        nbTrade = 0

        for i in range(0, len(predictions)):

            if predictions[i] > 0:
                nbTrade += 1

                if predictions[i] == self.yTest[i]:
                    nbGoodPred += 1

        if nbGoodPred == 0:
            return 0.0
        else:
            return round(nbGoodPred / nbTrade, 3)

    # retourne le nombre de trade effectué sur les données de test
    @staticmethod
    def getNbTrade(predictions):

        nbTrade = 0
        for pred in predictions:
            if pred > 0:
                nbTrade += 1
        return nbTrade

    # dresse des statistiques sur chaques modèles

    def setModelStat(self):

        self.logger.addLog("INFO", "Models", "Évaluation des modèles")
        stats = {}
        for k in self.models.keys():
            pred = self.getPredictions(self.models[k][0], self.models[k][1], self.xTest)
            stats[k] = [self.getAccuracy(pred), self.getTradeAccuracy(pred), self.getNbTrade(pred)]
        stats = pd.DataFrame(stats).transpose()
        stats.columns = ["acc", "accTra", "nbTrade"]
        self.stats = stats

    # sélectionne le meilleur modèle

    def setBestModel(self):

        bestStats = self.stats
        bestStats = bestStats[bestStats["nbTrade"] > 0]
        bestStats = bestStats[bestStats["acc"] > 0.5]
        bestStats = bestStats[bestStats["accTra"] > 0.1]
        bestStats = bestStats.sort_values(by=["acc", "accTra"], ascending=False)

        if bestStats.shape[0] < 1:
            bestModelType = self.stats.sort_values(by=["nbTrade", "acc", "accTra"], ascending=False).index[0]
            self.model = self.models[bestModelType]
            self.logger.addLog("INFO", "Models", "Meilleur modèle: {}".format(bestModelType))
        else:
            self.model = self.models[bestStats.index[0]]
            self.logger.addLog("INFO", "Models", "Meilleur modèle: {}".format(bestStats.index[0]))

    # créer un json récapitulaitf de la moulinette

    def getDictRecap(self, time):

        recap = self.conf
        recap["date"] = datetime.now()
        recap["nbModel"] = len(self.models)
        recap["time"] = str(time)

        modelRecaps = {}
        i = 0
        for k in self.models.keys():
            modelRecap = {"accuracy": self.stats.at[k, "acc"],
                          "tradeAccuracy": self.stats.at[k, "accTra"], "nbTrade": self.stats.at[k, "nbTrade"]}
            modelRecaps[k] = modelRecap
            i += 1

        recap["models"] = modelRecaps

        return recap

    # fait tourner la moulinette

    def run(self):

        self.logger.addLog("INFO", "Models", "Lancement moulinette de modèles")
        start = datetime.now().timestamp()
        self.models = {}
        self.linearSvc()
        pattern = self.getPatternToTrain(self.conf["nbNeurPerLayer"],
                                         self.conf["layerActivation"],
                                         int(self.conf["nbOutput"]))
        self.generateMlp(pattern, int(self.conf["batchSize"]), int(self.conf["epochs"]))
        self.setModelStat()
        self.setBestModel()
        self.saveModel()
        end = datetime.now().timestamp()
        recap = self.getDictRecap(timedelta(seconds=(end - start)))
        self.modelCol.insert_one(recap)

    # enregistre le modèle

    def saveModel(self):

        self.cleanModelDir()

        if self.model[1] == "keras":
            self.model[0].save(self.modelDir + self.model[1])
        elif self.model[1] == "sklearn":
            dump(self.model[0], self.modelDir + "sklearn.joblib")

        self.logger.addLog("INFO", "Models", "Sauvegarde du modèle")

    # charge le modèle

    def loadModel(self):

        self.logger.addLog("INFO", "Models", "Chargement du modèle")
        modelType = os.listdir(self.modelDir)

        if len(modelType) > 0:

            if modelType[0] == "keras":
                self.model = [load_model(self.modelDir + modelType[0]), modelType[0]]
            elif modelType[0] == "sklearn.joblib":
                self.model = [load(self.modelDir + "sklearn.joblib"), "sklearn"]

        else:

            self.model = None
            self.logger.addLog("WARNING", "Models", "Aucun modèle à charger")

    # supprime modèle existant

    def cleanModelDir(self):

        self.logger.addLog("INFO", "Models", "Suppresion des modèles")
        saveModelPath = os.listdir(self.modelDir)

        if len(saveModelPath) > 0:
            if saveModelPath[0] == "keras":
                shutil.rmtree(self.modelDir + saveModelPath[0])
            elif saveModelPath[0] == "sklearn.joblib":
                os.remove(self.modelDir + saveModelPath[0])
