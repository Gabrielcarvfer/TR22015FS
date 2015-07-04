#!/usr/bin/python

import thread
import time
import socket
import re
from uuid import getnode as get_mac


# Porta UDP para broadcast do keep alive
PORT = 12345
BROADCAST_IP = '255.255.255.255'
HOST_IP = ''
#Workaround to get public IP
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.connect(("gmail.com",80))
#HOST_IP = s.getsockname()[0]
#s.close()

def keepAliveListener(conn, LOCAL_IP, dict):
    while 1:
        # Receive messages
        while True:
            try:
                data, addr = conn.recvfrom(1028)
                if(addr[0] != LOCAL_IP):
                    #debug printing
                    #print "From addr: '%s', msg: '%s'" % (addr[0], data)

                    #filter source MAC address to match.group(1) and IP address to match.group(2)
                    match = re.match('SYNCFILES_MAC_(\d+)_IP_(.*$)', data)

                    #debug printing
                    #print match.group(1)
                    #print match.group(2)

                    #parse data into peer dictionary
                    if dict.has_key(match.group(1)):
                        #reset peer timer
                        continue

                    #if dict.has_key(match.group(1)):
                    else:
                        dict[match.group(1)] = match.group(2)
                        print 'New peer:' + dict[match.group(1)]
                        #set new peer timer
                        continue



                else:
                    print 'Message received was sent by myself'
                    continue
            except:
                print "timeout"

def keepAliveSend(conn, LOCAL_IP):
    while True:
            mac = get_mac()
            conn.sendto(('SYNCFILES_MAC_%s_IP_%s' % (mac, LOCAL_IP)), (BROADCAST_IP, PORT))
            time.sleep(1)

def startUDPServer(dict):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    LOCAL_IP = s.getsockname()[0]
    s.close()

    # Create socket and bind to address
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind((HOST_IP, PORT))
    udpSock.settimeout(5.0)

    udpSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    udpSock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)

    try:
        thread.start_new_thread( keepAliveListener, (udpSock, LOCAL_IP, dict, ) )
    except:
        print "Nao foi possivel iniciar thread Listener"

    try:
        thread.start_new_thread( keepAliveSend, (udpSock, LOCAL_IP,) )
    except:
        print "Nao foi possivel iniciar thread Sender"


    while 1:
        pass

    # Close socket
    udpSock.close()
    print 'UDP listener stopped.'









