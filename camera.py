import picamera
from time import sleep
import random
def takephoto():

    name = "photo"+ str(random.randint(0,99)) + ".jpg"
    with picamera.PiCamera() as camera:

        print("Get ready to take photo")

        sleep(5)

        camera.capture('/home/pi/MFRC522-python/static/image/'+name)

        print("photo take successfully")

        return name


