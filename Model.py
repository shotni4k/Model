import json
from loguru import logger
from numpy import ndarray
from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from error_handler.ErrorHandler import ErrorHandler
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

@dataclass(frozen=True)
class Test_set():
    X_test: list
    Y_test: list

@dataclass(frozen=True)
class DataSet():
    X_data: list
    Y_data: list


class LogisticRegressionModel():
    """ Класс Модели машинного обучения написанной на основе LogisticRegression() """
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = LogisticRegression()
        try:
            self.data_json = json.load(open('JsonFile/BOT_CONFIG.json'))
        except FileNotFoundError as error:
            logger.error(error)
    
    def _get_data_set(self) -> tuple:
        """ Метод разбивающий dataset на тренировочный и тестовый"""
        X = []
        Y = []

        for intent in self.data_json['intents'].keys():
            for example in self.data_json['intents'][intent]["examples"]:
                X.append(example), Y.append(intent)

        X_data,X_test,Y_data,Y_test = train_test_split(X,Y, test_size=0.2)
        
        return Test_set(X_test = X_test,Y_test = Y_test),DataSet(X_data =X_data, Y_data= Y_data)
        

    def model_test_train(self):
        """ Метод тестирующий модель """
        test_set = self._get_data_set()
        X_VectorsTest = self.vectorizer.fit_transform(test_set[0].X_test)
        self.classifier.fit(X_VectorsTest,test_set[0].Y_test)
        return logger.info(f"Приерная точность модели {self.classifier.score(X_VectorsTest, test_set[0].Y_test)}")

    def model_train(self):
        """ Метод тестирующий модель """
        data_set = self._get_data_set()
        X_Vectors = self.vectorizer.fit_transform(data_set[1].X_data)
        self.classifier.fit(X_Vectors,data_set[1].Y_data)
        return logger.info("Модель обученна")
        
    def get_intent(self,text:str) -> ndarray:
        """ Метод возвращающий интент"""
        return self.classifier.predict(self.vectorizer.transform([text]))