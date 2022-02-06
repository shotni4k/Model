import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from error_handler.ErrorHandler import ErrorHandler
from colorama import Back,Fore


class  LogisticRegressionModel():
    """ Класс Модели машинного обучения написанной на основе LogisticRegression() """
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier =  LogisticRegression()
        self.config = json.load(open(('jsonfile/BOT_CONFIG')))


    def get_data_set(self):
        """ Метод разбивающий dataset на тренировочный и тестовый"""
        x = []
        y = []

        for intent in self.config['intents'].keys():
            for example in self.config['intents'][intent]["examples"]:
                x.append(example),y.append(intent)

        train_test_split(x,y)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        self.model_test_trainig(X_test, y_test)

        return  self.model_training(X_train,y_train)
    

    def model_training(self,X_train,y_train):
        """ Метод обучающий модель  """
        # создание векторов
        self.vectorizer.fit(X_train)
        X_vectors = self.vectorizer.fit_transform(X_train)
        # обучение класификатора 
        self.classifier.fit(X_vectors,y_train)

      
        
    def model_test_trainig(self,X_test,y_test):
        """ Метод тестирующий модель """
        # Создание векторов
        self.vectorizer.fit(X_test)
        X_VectorsTest = self.vectorizer.fit_transform(X_test)
        # Обучение Класификатора
        self.classifier.fit(X_VectorsTest,y_test)
        return print(Fore.GREEN,f"Примерная точность модели {self.classifier.score(X_VectorsTest, y_test)}") 

    def get_intent_by_model(self,text):
        """ Метод возвращающий интент  """
        return self.classifier.predict(self.vectorizer.transform([text]))
        



model = LogisticRegressionModel()
error_handler = ErrorHandler()
try:
    model.get_data_set()
except FileNotFoundError as error:
    error_handler.save_errors(error)

