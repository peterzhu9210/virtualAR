#!/usr/bin/env python

import RPi.GPIO as GPIO
import array
import os

def read(id):

   list = []

   file_path = "/home/pi/MFRC522-python/static/information/"+id+".txt"
        
   if os.path.exists(file_path) == True:

        fo1 = open(file_path,"r")

        for line in open(file_path):
            line = fo1.readline()
            list.append(line)
        fo1.close()

   return list



