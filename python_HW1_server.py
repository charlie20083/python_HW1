import socket
import time

raddress = ('127.0.0.1', 68)
saddress = ('0.0.0.0', 3067)
daddress = ('0.0.0.0', 67)
i=2

def to_bytes(n, length, endianess='big'):
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]

while True:
    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    r.bind(('',3068))
    
    data, addr = r.recvfrom(2048)
    print "received:", data
#    r.close
#   r.unbind

    time.sleep(1)

#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#   s.bind(saddress)

#   msg = data[0:-40]+ '127.000.000.001' + ' 127.000.000.' + "%03d" % i + ' offer'

    packet = b''
    packet += b'\x02'
    packet += b'\x01'   #Hardware type: Ethernet
    packet += b'\x06'   #Hardware address length: 6
    packet += b'\x00'   #Hops: 0 
    packet += data[4:8]       #Transaction ID
    packet += b'\x00\x00'    #Seconds elapsed: 0
    packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
    packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
    packet += b'\x7f\x00\x00'   #Your (client) IP address: 127.0.0
    packet += to_bytes(i,1)
    packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
    #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
    packet += data[28:34]
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    packet += b'\x35\x01\x02'   #Option: (t=53,l=1) DHCP Message Type = DHCP Request
    #packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
    packet += b'\x3d\x06' + data[28:34]
    packet += b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
    packet += b'\xff'   #End Option

    r.sendto(packet, saddress)
    r.sendto(packet, daddress)
    print "replyed"
#   i=i+1
#   s.close
#   s.unbind

#   r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#   r.bind(raddress)

    data, addr = r.recvfrom(2048)
    print "received:", data
#   r.close

    time.sleep(1)

#   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#   s.bind(saddress)

#   msg = data[0:-39]+ '127.000.000.001' + ' 127.000.000.' + "%03d" % i + ' ACK'

    packet = b''
    packet += b'\x02'
    packet += b'\x01'   #Hardware type: Ethernet
    packet += b'\x06'   #Hardware address length: 6
    packet += b'\x00'   #Hops: 0 
    packet += data[4:8]       #Transaction ID
    packet += b'\x00\x00'    #Seconds elapsed: 0
    packet += b'\x80\x00'   #Bootp flags: 0x8000 (Broadcast) + reserved flags
    packet += b'\x00\x00\x00\x00'   #Client IP address: 0.0.0.0
    packet += b'\x7f\x00\x00'   #Your (client) IP address: 127.0.0
    packet += to_bytes(i,1)
    packet += b'\x00\x00\x00\x00'   #Next server IP address: 0.0.0.0
    packet += b'\x00\x00\x00\x00'   #Relay agent IP address: 0.0.0.0
    #packet += b'\x00\x26\x9e\x04\x1e\x9b'   #Client MAC address: 00:26:9e:04:1e:9b
    packet += data[28:34]
    packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'   #Client hardware address padding: 00000000000000000000
    packet += b'\x00' * 67  #Server host name not given
    packet += b'\x00' * 125 #Boot file name not given
    packet += b'\x63\x82\x53\x63'   #Magic cookie: DHCP
    packet += b'\x35\x01\x05'   #Option: (t=53,l=1) DHCP Message Type = DHCP ACK
    #packet += b'\x3d\x06\x00\x26\x9e\x04\x1e\x9b'   #Option: (t=61,l=6) Client identifier
    packet += b'\x3d\x06' + data[28:34]
    packet += b'\x37\x03\x03\x01\x06'   #Option: (t=55,l=3) Parameter Request List
    packet += b'\xff'   #End Option

    r.sendto(packet, saddress)
    r.sendto(packet, daddress)
    print "replyed"
    i=i+1
    r.close

