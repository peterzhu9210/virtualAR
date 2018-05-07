#!/usr/bin/env python

import RPi.GPIO as GPIO

def write(id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zapcode,rannum):

    fo = open('static/information/'+id+".txt","w")
    fo.write(id)
    fo.write("\n")
    fo.close()

    fo1 = open('static/information/'+id+".txt","a")
    fo1.write(fn+"\n")
    fo1.write(ln+"\n")
    fo1.write(cp+"\n")
    fo1.write(email+"\n")
    fo1.write(mp+"\n")
    fo1.write(wp+"\n")
    fo1.write(hp+"\n")
    fo1.write(ad+"\n")
    fo1.write(url+"\n")
    fo1.write(fb+"\n")
    fo1.write(tw+"\n")
    fo1.write(lk+"\n")
    fo1.write(yb+"\n")
    fo1.write(photo+"\n")
    fo1.write(zapcode+"\n")
    fo1.write(rannum+"\n")
    fo1.close()
