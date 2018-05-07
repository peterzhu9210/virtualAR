#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
from flask import Flask, render_template, request,url_for
import os
import socket
import fcntl
import struct
import array
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

reader = SimpleMFRC522.SimpleMFRC522()


print("Start reading your tag!")

try:
        id, info = reader.read()
        print("Your ID number is: " + info)
        print("Read done!\n")

        print("Start Loading Information!")
        info = info.strip(' ')

        fo1 = open('static/information/'+info+".txt","r")
        list = []

        for line in open('static/information/'+info+".txt"):
            line = fo1.readline()
            list.append(line)
        fo1.close()

        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template('test.html', id=info, photo = 'image/'+info+'.jpg',
                               fn = list[0],
                               ln = list[1],
                               cmp = list[2],
                               email = list[3],
                               mp = list[4],
                               wp = list[5],
                               hp = list[6],
                               pa = list[7].strip(','),
                               Web = list[8],
                               fb = list[9],
                               tw = list[10],
                               lk = list[11],
                               yb = list[12])

        @app.route('/information')
        def information():
            print(list[7])
            return render_template('id1.html', id = info,
                                fn = list[0],
                                ln  = list[1],
                                cmp = list[2],
                                email = list[3],
                                mp = list[4],
                                wp = list[5],
                                hp = list[6],
                                pa = list[7],
                                Web = list[8],
                                fb = list[9],
                                tw = list[10],
                                lk = list[11],
                                yb = list[12])

        @app.route('/image')
        def image():
              return render_template('image.html', filename='image/'+info+'.jpg')

        print("Information load done!\n")


        from_email = 'peterzhu9210@gmail.com'
        recipients_list = [list[3]]
        cc_list = []
        subject = info + '_Zapcode'
        message = 'Here is your ZapCode.'
        username = 'peterzhu9210@gmail.com'
        password = 'uiywycnkpovfntbg'
        server = 'smtp.gmail.com:587'

        def get_ip_address():
            SIOCGIFCONF = 0x8912
            SIOCGIFADDR = 0x8915
            BYTES = 4096
            sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            names = array.array('B',b'\0'*BYTES)
            bytelen = struct.unpack('iL',fcntl.ioctl(sck.fileno(), SIOCGIFCONF,
                            struct.pack('iL',BYTES,names.buffer_info()[0])))[0]
    
            namestr = names.tostring()
            ifaces = [namestr[i:i+32].split('\0',1)[0] for i in range(0,bytelen, 32)]

            iplist=""
            for ifname in ifaces:
                ip = socket.inet_ntoa(fcntl.ioctl(sck.fileno(),SIOCGIFADDR,struct.pack('256s',ifname[:15]))[20:24])
                if(ifname == "wlan0"):
                  iplist = ip
                  break

            return iplist
        
        ip = get_ip_address()

        homepage = "Home Page url: " + ip + ":5000"
        inf = "Information url: " + ip + ":5000/information"
        img = "Image url: " + ip + ":5000/image"

        message = message + '\n' + homepage + '\n' + inf + '\n' + img

        def sendmail(id,from_addr, to_addr_list, cc_addr_list, subject, message, login, password, smtpserver):
            msg = MIMEMultipart('related')
            msg['Subject'] = subject
            msg['From'] = from_addr
            msg['To'] = ";".join(to_addr_list)
            msg['Cc'] = ";".join(cc_addr_list)

            text_plain = MIMEText(message,'plain','utf-8')
            msg.attach(text_plain)

            image = MIMEImage(open('/home/pi/MFRC522-python/static/Zapcode/'+id+'.png','rb').read())
            image["Content-Disposition"] =  'attachment; filename = info + "_ZapCode.png"'
            msg.attach(image)

            server = smtplib.SMTP(smtpserver)
            server.starttls()
            server.login(login,password)
            problems = server.sendmail(from_addr, to_addr_list, msg.as_string())
            server.quit()

        sendmail(info,from_email, recipients_list, cc_list, subject, message, username, password, server)

        if __name__ == '__main__':
              app.run(debug = True, use_reloader=False, host='0.0.0.0')

finally:
        GPIO.cleanup()

