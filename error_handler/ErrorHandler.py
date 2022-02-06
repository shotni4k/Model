import json
import smtplib   
from datetime import datetime
from email.mime.multipart import MIMEMultipart      
from email.mime.text import MIMEText                
from email.mime.image import MIMEImage  

class ErrorHandler():
    def __init__(self):
        self.conig_data = json.load(open(('JsonFile/config.json')))
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()    
        self.server.login(self.conig_data["addr_from"],self.conig_data["password"])
    
    def send_message(self,text):
        msg = MIMEMultipart()
        msg['From'] = self.conig_data["addr_from"]
        msg['To'] = self.conig_data["addr_to"]
        msg['Subject'] = 'Ошибка у бота '  # Тема сообщения
        body = f'ошибка {text[0]}' # Техт сообщения 
        msg.attach(MIMEText(body, 'palin'))

        return self.server.send_message(msg)

  

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

        return self.send_message(text)

