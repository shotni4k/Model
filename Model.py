import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from colorama import Back,Fore


#(
#  1 - написать функцию для тестирования модели  
# )


class Model():
    """ Класс Модели машинного обучения написанной на основе LogisticRegression() """
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier =  LogisticRegression()


    def GetDataSet(self):
        """ Метод разбивающий dataset на тренировочный и тестовый"""
        from sklearn.model_selection import train_test_split
    
        X = []
        y = []

        try:
            with open('jsonfile/BOT_CONFIG.json',encoding='utf-8') as file:
                config = json.load(file)
        except FileNotFoundError as Error:
            from error_handler.ErrorHandler import SaveErrors
            print(Back.WHITE,Fore.RED,"Отсутсвует Json-file")
            SaveErrors(Error)
            
        for intent in config['intents'].keys():
            for example in config['intents'][intent]["examples"]:
                X.append(example),y.append(intent)

        train_test_split(X,y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.ModelTestTrainig(X_test, y_test)
        return  self.ModelTraining(X_train,y_train)
    

    def ModelTraining(self,X_train,y_train):
        """ Метод обучающий модель  """
        # создание векторов
        self.vectorizer.fit(X_train)
        X_vectors = self.vectorizer.fit_transform(X_train)
        # обучение класификатора 
        self.classifier.fit(X_vectors,y_train)
      
        
    def ModelTestTrainig(self,X_test,y_test):
        """ Метод тестирующий модель """
        # Создание векторов
        self.vectorizer.fit(X_test)
        X_VectorsTest = self.vectorizer.fit_transform(X_test)
        # Обучение Класификатора
        self.classifier.fit(X_VectorsTest,y_test)
        return print(Fore.GREEN,f"Примерная точность модели {self.classifier.score(X_VectorsTest, y_test)}") 

    def GetIntentByModel(self,text):
        """ Метод возвращающий интент  """
        return self.classifier.predict(self.vectorizer.transform([text]))
        



model = Model()
def start():
    model.GetDataSet()

while True:
    try:
        start()
        text = input("Напиши текст \n")
        print(model.GetIntentByModel(text))
    finally:
        print("Приложкние завершило работу")
