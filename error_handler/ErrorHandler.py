def SaveErrorsEmail(text):
    """ Функция отпровляющая сообщение об ошибке на почту"""
    #(
    # 1- не ктотырые вещи можно вынести в списки
    # )
    import smtplib   
    from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
    from email.mime.text import MIMEText                # Текст/HTML
    from email.mime.image import MIMEImage  

    addr_from = '----------' # Адресат 
    addr_to  = '----------'  # Получатель
    password = '----------'  # Пороль
    
    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to    
    msg['Subject'] = 'Ошибка у бота '  # Тема сообщения
    body = f'ошибка {text[0]}' # Техт сообщения 
    msg.attach(MIMEText(body, 'palin'))

    server = smtplib.SMTP('smtp.gmail.com', 587) # обьект SMPT
    server.set_debuglevel(False) 
    server.starttls() # Начинаем шифрованный обмен по TLS
    server.login(addr_from,password) # Авторизация
    server.send_message(msg) # Отправка сообщения 
    server.quit()
    return 

def SaveErrors(Error):
    import json
    from datetime import datetime
    
    
    text =[]
    text.append({
                    'error': Error,
                    'data': datetime.now().date(),
                    'time': datetime.now().time(),
                 },)
    with open('errors/errors.json','w',encoding= 'utf-8') as errors:
          errors.write(json.dumps(  text,
                                    ensure_ascii = False,
                                    indent = 4,
                                    sort_keys= True,
                                    default= str
                                    ))

    return save_errors_email(text)
