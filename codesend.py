import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_email = 'peterzhu9210@gmail.com'
recipients_list = ['peterzhu9210@gmail.com']
cc_list = []
subject = 'ZapCode'
message = 'Here is your ZapCode.'
username = 'peterzhu9210@gmail.com'
password = 'uiywycnkpovfntbg'
server = 'smtp.gmail.com:587'

def sendemail(from_addr, to_addr_list, cc_addr_list, subject, message, login, password, smtpserver):

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ";".join(to_addr_list)
    msg['Cc'] = ";".join(cc_addr_list)

    text_plain = MIMEText(message,'plain','utf-8')
    msg.attach(text_plain)
    
    image = MIMEImage(open('/home/pi/MFRC522-python/static/image/ZapCode.png','rb').read())
    image["Content-Disposition"] = 'attachment; filename ="10414708ZapCode.png"'
    msg.attach(image)

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, msg.as_string())
    server.quit()

sendemail(from_email, recipients_list, cc_list, subject, message, username, password, server) 
