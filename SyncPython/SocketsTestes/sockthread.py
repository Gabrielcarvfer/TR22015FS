#!/usr/bin/python

import thread
import time
import socket

# Porta UDP para broadcast do keep alive
PORT = 1234
#keepAliveMSG = "EstouVivo!"+str(id)

def keepAliveListener(conn):
    while 1:
        # Receive messages
        while True:
            try:
                data, addr = conn.recvfrom(1028)
                print "From addr: '%s', msg: '%s'" % (addr[0], data)
            except:
                print "timeout"


# cs = socket(AF_INET, SOCK_DGRAM)
# cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

def keepAliveSend(conn):
    while True:
            conn.sendto('to vivo doodio', ('255.255.255.255', 1234))
            time.sleep(1)

# Create socket and bind to address
udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSock.bind(('', PORT))
udpSock.settimeout(5.0)

# cs = socket(AF_INET, SOCK_DGRAM)
# cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
udpSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
udpSock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)

try:
    thread.start_new_thread( keepAliveListener, (udpSock, ) )
except:
    print "Nao foi possivel iniciar thread Listener"

try:
    thread.start_new_thread( keepAliveSend, (udpSock, ) )
except:
    print "Nao foi possivel iniciar thread Sender"


while 1:
    pass

# Close socket
udpSock.close()
print 'UDP listener stopped.'









