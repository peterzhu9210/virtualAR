#!/usr/bin/env python


from flask import Flask, render_template, request, url_for
import os

app = Flask(__name__)

info = raw_input("Please input ID number: ")

fo1 = open('/home/pi/MFRC522-python/static/information/'+info+".txt","r")
list = []

for line in open('/home/pi/MFRC522-python/static/information/'+info+".txt"):
     line = fo1.readline()
     list.append(line)
fo1.close()

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
                               pa = list[7],
                               Web = list[8],
                               fb = list[9],
                               tw = list[10],
                               lk = list[11],
                               yb = list[12])

@app.route('/information')
def information():
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
	return render_template('image.html', filename = 'image/'+info+'.jpg')

if __name__ == '__main__':
   app.run(debug=True, use_reloader=False, host='0.0.0.0')
