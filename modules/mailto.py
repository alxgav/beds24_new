import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

#const

# USER = 'myroomtopapartment@gmail.com'
# KEY = 'MyRoom135.#'
USER = 'alxgav@gmail.com'
KEY = 'NIK06Jerzy04'

def send_email(SUBJECT ='subject', FROM = 'mail@mail.com', TO = ['mail@mail.com'], content = 'any message'):
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT 
    msg['From'] = FROM
    msg['To'] = ','.join(TO)
    msg.add_header('Content-Type','text/html')

    html = f'{content}'
    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(USER, KEY)
    server.sendmail(msg['From'], TO, msg.as_string())
    server.quit() 
    print ('message sends', msg['To'])