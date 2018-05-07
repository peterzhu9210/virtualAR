#!/usr/bin/env python

from flask import Flask, render_template, request,redirect,url_for
import webbrowser
import database as db
import camera as cam
import GetIp as gip
import W_file as wf
import R_file as rf
import file_delete as df
import os
import string
import RPi.GPIO as GPIO
import SimpleMFRC522
import random
import urllib
import EmailSend as es
import re

reader= SimpleMFRC522.SimpleMFRC522()

ip_address = gip.get_ip_address()

db.link_database(ip_address)

id = "0"
name = "photo"
global cus_info
global del_cus
cus_info = "0"
del_cus = "0"

app = Flask(__name__)



@app.route('/')
def index():
    return render_template("main.html")



@app.route('/new_customer', methods=["GET","POST"])
def new_customer():
    if request.method == 'POST':
       if request.form.get('Take Photo') == 'Take Photo':
          photo_name = request.values.get("idphoto")
          if (len(photo_name) == 0) | (string.find(photo_name,ip_address) != -1):
             global name
             name = cam.takephoto()
             photo_name = ip_address + ":5000/preview.jpg"
             print("Take Photo")
             source="static/image/"+name
             print(source)
             return render_template("new_cus.html",
                                 photo=photo_name,
                                 preview=u'<strong>Photo Preview</strong>', 
                                 preview_photo=u'<img src ="' + source + '" width="256" height="256"/><br /><br />')
          else:
             photo_name = request.values.get("idphoto")
             return render_template("new_cus.html",
                                    photo = photo_name,
                                    preview=u'<strong>Photo Preview</strong>',
                                    preview_photo=u'<img src="' + photo_name + '" width="256" height="256"/><br /><br />')
       elif request.form.get('Create User') == 'Create User':
          global id
          id = request.values.get("id")
          fn = request.values.get("First Name")
          ln = request.values.get("Last Name")
          cp = request.values.get("Company")
          email = request.values.get("Email")
          mp = request.values.get("MobileP")
          wp = request.values.get("WorkP")
          hp = request.values.get("HomeP")
          ad = request.values.get("Address")
          url = request.values.get("Website")
          fb = request.values.get("facebook")
          tw = request.values.get("twitter")
          lk = request.values.get("linkedin")
          yb = request.values.get("youtube")
          photo = request.values.get("idphoto")
          if string.find(photo,ip_address) != -1:
             print("rename")
             new_name= "/home/pi/MFRC522-python/static/image/"+id+".jpg"
             old_name="/home/pi/MFRC522-python/static/image/" + name
             if os.path.exists(old_name):
                os.rename(old_name,new_name)
                df.delete('/home/pi/MFRC522-python/static/image/','photo')
             photo = "localhost:5000/" + id + ".jpg"
             zap = request.values.get("zapcode")
             zap_name = '/home/pi/MFRC522-python/static/Zapcode/'+id+'.png'

             cus_info = str(random.randint(0,9999))

             wf.write(id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             reader.write(id)
             GPIO.cleanup()

             db.Insert("Customer",id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             urllib.urlretrieve(zap,zap_name)

             print("Create")
          else:
             zap = request.values.get("zapcode")
             zap_name = '/home/pi/MFRC522-python/static/Zapcode/'+id+'.png'

             df.delete('/home/pi/MFRC522-python/static/image/','photo')
             cus_info = str(random.randint(0,9999))

             wf.write(id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             reader.write(id)
             GPIO.cleanup()

             db.Insert("Customer",id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             urllib.urlretrieve(zap,zap_name)
             print("Create")

          return redirect(url_for('existed_customer'))
    elif request.method == 'GET':
          print("No call")
    return render_template("new_cus.html")



@app.route('/existed_customer',methods=["GET","POST"])
def existed_customer():


    if request.method  == 'POST':
       if request.form.get('Edit Information') == 'Edit Information':
          return redirect(url_for('customer_edit'))
    elif request.method == 'GET':
          global id
          info,id = reader.read()
          GPIO.cleanup()
          id = id.strip(' ')

          list = rf.read(id)
          if len(list):
             global cus_info
             cus_info = list[16]
             print(cus_info)
             info = ip_address + ":5000/existed_customer/"+ id + "_" + cus_info
             zap_path = "/home/pi/MFRC522-python/static/Zapcode/" + id +".png"
             es.send(id,list[4],info,zap_path)
             if string.find(list[14],"localhost") != -1:
                list[14] = "image/" + id + ".jpg"
                print(list[14])
                return render_template('existed_cus.html',id = list[0],fn = list[1],
                                 ln = list[2],
                                 cp = list[3],
                                 em = list[4],
                                 mp = list[5],
                                 wp = list[6],
                                 hp = list[7],
                                 ad = list[8],
                                 url = list[9],
                                 fb = list[10],
                                 tw = list[11],
                                 lk = list[12],
                                 yb = list[13],
                                 photo = list[14],
                                 zapcode = list[15])
             else:
                return render_template('existed_cus1.html',id = list[0],fn = list[1],
                                 ln = list[2],
                                 cp = list[3],
                                 em = list[4],
                                 mp = list[5],
                                 wp = list[6],
                                 hp = list[7],
                                 ad = list[8],
                                 url = list[9],
                                 fb = list[10],
                                 tw = list[11],
                                 lk = list[12],
                                 yb = list[13],
                                 photo = list[14],
                                 zapcode = list[15] )
          else:
             return redirect(url_for('no_cus'))

    return render_template("existed_cus.html")



@app.route('/no_cus')
def no_cus():
    global id
    return render_template("no_cus.html",id=id)



@app.route('/existed_customer/<id>_<cus_info>')
def existed_customer_id(id,cus_info):
    list=[]
    list = rf.read(id)
    if len(list):
       if string.find(list[14],"localhost") != -1:
          list[14] = "image/" + id + ".jpg"
          print(list[14])
          return render_template('existed_cus_unc.html',id = list[0],fn = list[1],
                                 ln = list[2],
                                 cp = list[3],
                                 em = list[4],
                                 mp = list[5],
                                 wp = list[6],
                                 hp = list[7],
                                 ad = list[8],
                                 url = list[9],
                                 fb = list[10],
                                 tw = list[11],
                                 lk = list[12],
                                 yb = list[13],
                                 photo = list[14],
                                 zapcode = list[15])
       else:
          return render_template('existed_cus1_unc.html',id = list[0],fn = list[1],
                                 ln = list[2],
                                 cp = list[3],
                                 em = list[4],
                                 mp = list[5],
                                 wp = list[6],
                                 hp = list[7],
                                 ad = list[8],
                                 url = list[9],
                                 fb = list[10],
                                 tw = list[11],
                                 lk = list[12],
                                 yb = list[13],
                                 photo = list[14],
                                 zapcode = list[15] )

    return render_template("existed_cus_unc.html")


@app.route('/customer_edit',methods=["GET","POST"])
def edit():
    if request.method == 'POST':
       if request.form.get('Change Photo') == 'Change Photo':
          photo_name = request.values.get("idphoto")
          list = []
          list = rf.read(id)
          if (len(photo_name) == 0) | (string.find(photo_name,ip_address) != -1) | (string.find(photo_name,"localhost") != -1):
             global name
             name = cam.takephoto()
             photo_name = ip_address + ":5000/"+name
             source="/static/image/"+name
             return render_template("edit_cus.html",
                                 photo=photo_name,
                                 photo_preview = source,
                                 id = list[0],
                                 fn = list[1],
                                 ln = list[2],
                                 cp = list[3],
                                 em = list[4],
                                 mp = list[5],
                                 wp = list[6],
                                 hp = list[7],
                                 ad = list[8],
                                 url = list[9],
                                 fb = list[10],
                                 tw = list[11],
                                 lk = list[12],
                                 yb = list[13],
                                 zapcode = list[15])
          else:
             photo_name = request.values.get("idphoto")
             return render_template("edit_cus.html",
                                    photo = photo_name,
                                    photo_preview = photo_name,
                                    id = list[0],
                                    fn = list[1],
                                    ln = list[2],
                                    cp = list[3],
                                    em = list[4],
                                    mp  = list[5],
                                    wp = list[6],
                                    hp = list[7],
                                    ad = list[8],
                                    url = list[9],
                                    fb = list[10],
                                    tw = list[11],
                                    lk = list[12],
                                    yb = list[13],
                                    zapcode = list[15])
       elif request.form.get('Edit Done') == 'Edit Done':
          global id
          fn = request.values.get("First Name")
          ln = request.values.get("Last Name")
          cp = request.values.get("Company")
          email = request.values.get("Email")
          mp = request.values.get("MobileP")
          wp = request.values.get("WorkP")
          hp = request.values.get("HomeP")
          ad = request.values.get("Address")
          url = request.values.get("Website")
          fb = request.values.get("facebook")
          tw = request.values.get("twitter")
          lk = request.values.get("linkedin")
          yb = request.values.get("youtube")
          photo = request.values.get("idphoto")
           
          if (string.find(photo,ip_address) != -1) | (string.find(photo,"localhost") != -1):
             new_name= "/home/pi/MFRC522-python/static/image/" + id + ".jpg"
             old_name="/home/pi/MFRC522-python/static/image/" + name
             if os.path.exists(old_name):
                os.rename(old_name,new_name)
                df.delete('/home/pi/MFRC522-python/static/image/','photo')
             photo = "localhost:5000/" + id + ".jpg"
             zap = request.values.get("zapcode")
             zap_name = '/home/pi/MFRC522-python/static/Zapcode/'+id+'.png'

             wf.write(id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             reader.write(id)
             GPIO.cleanup()

             db.Edit("Customer",id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             urllib.urlretrieve(zap,zap_name)
             print("Edit")
          else:
             zap = request.values.get("zapcode")
             zap_name = '/home/pi/MFRC522-python/static/Zapcode/'+id+'.png'

             df.delete('/home/pi/MFRC522-python/static/image/','photo')
             wf.write(id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             reader.write(id)
             GPIO.cleanup()

             db.Edit("Customer",id,fn,ln,cp,email,mp,wp,hp,ad,url,fb,tw,lk,yb,photo,zap,cus_info)

             urllib.urlretrieve(zap,zap_name)
             print("Edit")

          return redirect(url_for('existed_customer'))
    elif request.method == 'GET':
          print("No call")

    print(id)
    list = []
    list = rf.read(id)
    print(list[14])
    if len(list):
       if string.find(list[14],"localhost") != -1:
             source = "static/image/"+id+".jpg"
             print(source)
             return render_template("edit_cus.html",
                                 photo = list[14],
                                 photo_preview = source,
                                 id = list[0],
                                 fn = list[1],
                                 ln = list[2],
                                 cp = list[3],
                                 em = list[4],
                                 mp = list[5],
                                 wp = list[6],
                                 hp = list[7],
                                 ad = list[8],
                                 url = list[9],
                                 fb = list[10],
                                 tw = list[11],
                                 lk = list[12],
                                 yb = list[13],
                                 zapcode = list[15])
       else:
             photo_name = list[14]
             return render_template("edit_cus.html",
                                    photo = list[14],
                                    photo_preview = photo_name,
                                    id = list[0],
                                    fn = list[1],
                                    ln = list[2],
                                    cp = list[3],
                                    em = list[4],
                                    mp  = list[5],
                                    wp = list[6],
                                    hp = list[7],
                                    ad = list[8],
                                    url = list[9],
                                    fb = list[10],
                                    tw = list[11],
                                    lk = list[12],
                                    yb = list[13],
                                    idphoto = list[14],
                                    zapcode = list[15])
    else:
       return render_template("edit_cus.html")



@app.route('/delete_customer', methods=["GET","POST"])
def delete_cus():
    if request.method == 'POST':
       if request.form.get('Read ID') == 'Read ID':
          global id
          info,id = reader.read()
          id = id.strip(" ")
          return render_template("del_cus.html",id=id)
       elif request.form.get('Delete User') == 'Delete User':
          global del_cus
          global id
          id = request.values.get("ID")
          if os.path.exists("/home/pi/MFRC522-python/static/image/" + id + ".jpg"):
             os.remove(os.path.join("/home/pi/MFRC522-python/static/image/", id+".jpg"))
          if os.path.exists("/home/pi/MFRC522-python/static/information/" + id + ".txt"):
             os.remove(os.path.join("/home/pi/MFRC522-python/static/information/",id +".txt"))
          if os.path.exists("/home/pi/MFRC522-python/static/Zapcode/" + id + ".png"):
             os.remove(os.path.join("/home/pi/MFRC522-python/static/Zapcode/",id + ".png"))

          temp = str(db.Select("Customer",id,"RANNUMBER"))
          temp = re.findall(r"\d+",temp)

          if len(temp) != 0:
             db.Delete("Customer",id)
          else:
             return render_template("del_cus.html",message='<label>Customer No: \'' + id + '\' does not exist!</label><br /><br /><br />')
    
    return render_template("del_cus.html")


@app.route('/existed_customer/<id>_<del_cus>')
def delete_web():
    global id
    global del_cus
    print(del_cus)
    return render_template("not_found.html")



@app.route('/photo.jpg')
def photo():
    print(id)
    return render_template("image.html", filename='image/'+ id + '.jpg')


if __name__ == '__main__':
   app.run(debug=True, use_reloader=False, host='0.0.0.0') 


