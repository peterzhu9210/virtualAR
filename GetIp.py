import socket
import fcntl
import struct
import array

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

print(get_ip_address())
