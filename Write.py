#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import picamera
from time import sleep
import database as db

reader = SimpleMFRC522.SimpleMFRC522()

try:
        text = raw_input("Please input your ID Number: ")
	input = raw_input('Create a new user?(y/n)')
	if (input == 'y') | (input == 'Y'):
           fo = open('static/information/'+text+".txt","w")

           fn = raw_input("First_Name: ")
           fo.write(fn)
           fo.write("\n")
           fo.close()

           fo1 = open('static/information/'+text+".txt","a")

           ln = raw_input("Last_Name: ")
           fo1.write(ln)
           fo1.write("\n")

           cp = raw_input("Company: ")
           fo1.write(cp)
           fo1.write("\n")

           em = raw_input("Email: ")
           fo1.write(em)
           fo1.write("\n")

           mp = raw_input("Mobile Phone: ")
           fo1.write(mp)
           fo1.write("\n")

           wp = raw_input("Work Phone: ")
           fo1.write(wp)
           fo1.write("\n")

           hp = raw_input("Home Phone: ")
           fo1.write(hp)
           fo1.write("\n")

           add = raw_input("Address: ")
           fo1.write(add)
           fo1.write("\n")

           url = raw_input("Website URL: ")
           fo1.write(url)
           fo1.write("\n")

           fb = raw_input("Facebook Username: ")
           fo1.write(fb)
           fo1.write("\n")

           tw = raw_input("Twitter Username: ")
           fo1.write(tw)
           fo1.write("\n")

           lk = raw_input("Linkedin Username: ")
           fo1.write(lk)
           fo1.write("\n")

           ytb = raw_input("Youtube Username: ")
           fo1.write(ytb)

           fo1.close()

           db.store_in_database(text,fn,ln,cp,em,mp,wp,hp,add,url,fb,tw,lk,ytb)

           print("Now place your tag to wrtie!") 
           reader.write(text)

	   print("Written")

           photo = raw_input("Want to take photo?(y/n)")

           if (photo == 'y')|(photo == 'Y'):
           
              print("Get ready to take photo!")

              sleep(8)

              with picamera.PiCamera() as camera:

                   print("Smile!")

                   sleep(5)

                   camera.capture('/home/pi/MFRC522-python/static/image/'+ text +'.jpg')

                   print("Photo is done!")
   	else:

	   print("Now place your tag to write")
	   reader.write(text)
     	   print("Written") 
finally:
	GPIO.cleanup()


