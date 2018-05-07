#!/usr/bin/env python

import os
import socket
import fcntl
import struct
import array
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(id,reci_email,info,zap):
        from_email = 'peterzhu9210@gmail.com'
        recipients_list = [reci_email]
        cc_list = []
        subject = id + '_Zapcode'
        message = 'Here is your Information and ZapCode.'
        username = 'peterzhu9210@gmail.com'
        password = 'uiywycnkpovfntbg'
        server = 'smtp.gmail.com:587'

        message = message + '\n' + info

        def sendmail(id,from_addr, to_addr_list, cc_addr_list, subject, message, login, password, smtpserver):
            msg = MIMEMultipart('related')
            msg['Subject'] = subject
            msg['From'] = from_addr
            msg['To'] = ";".join(to_addr_list)
            msg['Cc'] = ";".join(cc_addr_list)

            text_plain = MIMEText(message,'plain','utf-8')
            msg.attach(text_plain)

            image = MIMEImage(open(zap,'rb').read())
            image["Content-Disposition"] =  'attachment; filename = info + "_ZapCode.png"'
            msg.attach(image)

            server = smtplib.SMTP(smtpserver)
            server.starttls()
            server.login(login,password)
            problems = server.sendmail(from_addr, to_addr_list, msg.as_string())
            server.quit()

        sendmail(info,from_email, recipients_list, cc_list, subject, message, username, password, server)
