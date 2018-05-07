import database as db
import re

ip = db.get_ip_address()

db.link_database(ip)

data = db.Select("Customer","2","RANNUMBER")

data = str(data)

data = "s" + data

data = re.findall(r"\d+",data)

data1 = data[0]

data1 = "b" + data1 + "a"
print(data1)

db.Close_database()
