from random import Random
import socket
import time
import os

rnd = Random()
rnd.seed()

saddress = ('0.0.0.0', 3068)
daddress = ('0.0.0.0' , 68)
#raddress = ('127.0.0.1', 3067)

def genmac():
    i = []
    for z in xrange(6):
        i.append(rnd.randint(0,255))
    return ''.join(map(lambda x:"%02x"%x,i))

def genxid(): 
    i = []
    for z in xrange(4):
        i.append(rnd.randint(0,255))
    return ''.join(map(lambda x:"%02x"%x,i))

rtime=raw_input()

for x in range(int(rtime)):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('',3067))

    tmac=os.urandom(6)
    txid=os.urandom(4)
    

    packet = b''
    packet += b'\x01'   #Message type: Boot Request (1)
    packet += b'\x01'   #Hardware type: Ethernet
    packet += b'\x06'   #Hardware address length: 6
    packet += b'\x00'   #Hops: 0 
    packet += txid       #Transaction ID
    packet += b'\x00\x00'    #Seconds elapsed: 0
    packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
    packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
    #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
    packet += tmac
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
    #packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
    packet += b'\x3d\x06' + tmac
    packet += b'\x37\x01\x01'   #Option: (t=55,l=3) Parameter Request List
    packet += b'\xff'   #End Option


#   msg=tmac + ' ' + txid + ' 000.000.000.000'*2 + ' discover'

    print packet
    print packet[2]

    s.sendto(packet, saddress)
    s.sendto(packet, daddress)
#   s.close
#   s.unbind

#   time.sleep(1)

#   r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#   r.bind(raddress)

    data,addr=s.recvfrom(2048)
    
    print "received: " + data

#   r.close

    time.sleep(1)

#   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
#   msg=tmac + ' ' + txid + ' 000.000.000.000'*2 + ' request'
    
    packet = b''
    packet += b'\x01'   #Message type: Boot Request (1)
    packet += b'\x01'   #Hardware type: Ethernet
    packet += b'\x06'   #Hardware address length: 6
    packet += b'\x00'   #Hops: 0 
    packet += data[4:8]       #Transaction ID
    packet += b'\x00\x00'    #Seconds elapsed: 0
    packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
    packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Your (client) IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
    #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
    packet += data[28:34]
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    packet += b'\x35\x01\x03'   #Option: (t=53,l=1) DHCP Message Type = DHCP Request
    #packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
    packet += b'\x3d\x06' + data[28:34]
    packet += b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
    packet += b'\xff'   #End Option

    s.sendto(packet, saddress)
    s.sendto(packet, daddress)
#   s.close

#   r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#   r.bind(raddress)

    data,addr=s.recvfrom(2048)

    print "received: " + data

    s.close

    time.sleep(1)
    


#   r.unbind
