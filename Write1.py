#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import picamera
from time import sleep
import database as db

reader = SimpleMFRC522.SimpleMFRC522()

try:
        text = raw_input("Please input your ID Number: ")
	reader.write(text)

	print("Written")

finally:
	GPIO.cleanup()


