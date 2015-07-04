#!/usr/bin/python

import thread
import time
import socket

# Porta UDP para broadcast do keep alive
PORT = 12345
BROADCAST_IP = '255.255.255.255'
HOST_IP = ''
#Workaround to get public IP
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("gmail.com",80))
#HOST_IP = s.getsockname()[0]
#s.close()

def keepAliveListener(conn):
    while 1:
        # Receive messages
        while True:
            try:
                data, addr = conn.recvfrom(1028)
                print "From addr: '%s', msg: '%s'" % (addr[0], data)
                #parse data into peer dictionary
            except:
                print "timeout"

def keepAliveSend(conn):
    while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com",80))
            localIP = s.getsockname()[0]
            s.close()
            conn.sendto(('SYNCFILES_LocalIP',localIP,'_PeerIP',s.getpeername()[0],), (BROADCAST_IP, PORT))
            time.sleep(1)

def startUDPServer():
    # Create socket and bind to address
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind((HOST_IP, PORT))
    udpSock.settimeout(5.0)

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









