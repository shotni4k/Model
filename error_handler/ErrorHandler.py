import json
import smtplib   
from datetime import datetime
from email.mime.multipart import MIMEMultipart      
from email.mime.text import MIMEText                
from email.mime.image import MIMEImage  

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Work_To_Email(metaclass = MetaSingleton):
    connection = None

    def __init__(self):
        self.conig_data = json.load(open(('JsonFile/config.json')))
        self.server = smtplib.SMTP('smtp.gmail.com', 587) 
        self.server.set_debuglevel(False) 
        self.server.starttls() 
        self.server.login(self.conig_data["addr_from"],self.conig_data["password"]) 

    
    def send_message(self,text):
        msg = MIMEMultipart()
        msg['From'] = self.conig_data["addr_from"]
        msg['To'] = self.conig_data["addr_to"]
        msg['Subject'] = 'Ошибка у бота '  
        body = str(text)
        msg.attach(MIMEText(body, 'palin'))
        self.server.send_message(msg)
        return self.server.quit()

class ErrorHandler():

    def save_errors(self,error):
        text =[]
        text.append({
                    'error': error,
                    'data': datetime.now().date(),
                    'time': datetime.now().time(),
                 },)
        with open('JsonFile/errors.json','w',encoding= 'utf-8') as errors:
            errors.write(json.dumps(  text,
                                      ensure_ascii = False,
                                      indent = 4,
                                      sort_keys= True,
                                      default= str
                                    ))
        return Work_To_Email().send_message(text)

