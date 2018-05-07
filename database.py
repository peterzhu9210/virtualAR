import MySQLdb as mdb
import array
import socket
import fcntl
import struct

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


def link_database(ip):

  print("Your Ip is " + ip)
  print("Linking to Database...")
  global conn
  conn = mdb.connect(host=ip,user='root"',passwd='ZHUzhu92',db='customerinfo',charset='utf8')
  print("Link database successfully!")

def Create_Table(table_name):
    cur=conn.cursor()
    sql_Create_Table = "CREATE TABLE " + table_name + " (ID VARCHAR(255),FIRST_NAME VARCHAR(255), LAST_NAME VARCHAR(255), COMPANY VARCHAR(255),EMAIL VARCHAR(255), MOBILEP VARCHAR(255), WORKP VARCHAR(255), HOMEP VARCHAR(255), ADDRESS VARCHAR(255), WEBSITE VARCHAR(255), FACEBOOK VARCHAR(255), TWITTER VARCHAR(255), LINKEDIN VARCHAR(255), YOUTUBE VARCHAR(255), PHOTO VARCHAR(255), ZAPCODE VARCHAR(255), RANNUMBER VARCHAR(255), PRIMARY KEY(ID))ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    cur.execute(sql_Create_Table)
    conn.commit()
    cur.close()

def Drop_Table(table_name):
    cur = conn.cursor()
    sql_Delete_Table = "Drop Table " + table_name
    cur.execute(sql_Delete_Table)
    conn.commit()
    cur.close()

def Select(table_name,id,item):
    cur = conn.cursor()
    sql_Select = "SELECT " + item + " FROM " + table_name + " where id = " + id + " ;"
    cur.execute(sql_Select)
    data = cur.fetchone()
    conn.commit()
    cur.close()
    return data

def Insert(table_name,id,fn,ln,cp,em,mp,wp,hp,ad,url,fb,tw,lk,ytb,photo,zapcode,rannum):
    cur = conn.cursor()
    sql_Insert1 = "INSERT INTO customerinfo."+ table_name +"(ID,FIRST_NAME,LAST_NAME,COMPANY,EMAIL,MOBILEP,WORKP,HOMEP,ADDRESS,WEBSITE,FACEBOOK,TWITTER,LINKEDIN,YOUTUBE,PHOTO,ZAPCODE,RANNUMBER)"
    sql_Insert2 = "VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"
    sql_Insert = sql_Insert1 + sql_Insert2
    cur.execute(sql_Insert%(id,fn,ln,cp,em,mp,wp,hp,ad,url,fb,tw,lk,ytb,photo,zapcode,rannum))
    conn.commit()
    cur.close()

def Delete(table_name,id):
    cur = conn.cursor()
    sql_Delete ="Delete FROM " + table_name + " where ID = " + id +";"
    cur.execute(sql_Delete)
    conn.commit()
    cur.close()

def Edit(table_name,id,fn,ln,cp,em,mp,wp,hp,add,url,fb,tw,lk,ytb,photo,zapcode,rannum):
    Delete(table_name,id)
    Insert(table_name,id,fn,ln,cp,em,mp,wp,hp,add,url,fb,tw,lk,ytb,photo,zapcode,rannum)

def Close_database():
    conn.close()

