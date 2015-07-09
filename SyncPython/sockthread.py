#!/usr/bin/python

import thread
import time
import socket
import re
import threading
from uuid import getnode as get_mac
import gvar


# Porta UDP para broadcast do keep alive
PORT = 54321
BROADCAST_IP = '255.255.255.255'
threads = []
#HOST_IP = ''


def keepAliveListener(conn):
    # Receive messages
    while True:
        try:
            data, addr = conn.recvfrom(1028)
            # debug printing
            #print "From addr: '%s', msg: '%s'" % (addr[0], data)

            # filter source MAC address to match.group(1) and IP address to match.group(2)
            match = re.match('SYNCFILES_MAC_(\d+)_IP_(.*$)', data)

            # debug printing
            #print match.group(1)
            #print match.group(2)

            # parse data into peer dictionary
            #if dict.has_key(match.group(1)):
            #TODO: reset peer timer
            #    continue

            mac_long = long(match.group(1))
            if mac_long in gvar.peer_dict:
                if gvar.peer_dict[mac_long][0] == match.group(2):
                    #set peer as alive

                    gvar.peer_dict.update({mac_long :(match.group(2), 1)})
                    continue
            else:
                #add new peer and set as alive
                gvar.peer_dict[mac_long] = (match.group(2),1)
                #print 'New peer:' + dict[match.group(1)]
                continue
        except:
            print "timeout"
        time.sleep(0.1)


def keepAliveSend(conn):
    while True:
        conn.sendto(('SYNCFILES_MAC_%s_IP_%s' % (gvar.mac, gvar.ip)), (BROADCAST_IP, PORT))
        time.sleep(0.5)

def keepAlivePeers():
    while True:
        time.sleep(33)
        for peers in gvar.peer_dict:
            peer_ip = gvar.peer_dict[peers][0]
            gvar.peer_dict.update({peers: (peer_ip, 0)})

def getSockMac():
    return get_mac()

def getLocalIP():
    # workaround to get local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    LOCAL_IP = s.getsockname()[0]
    s.close()
    return LOCAL_IP

def UDPServer():

    # Create socket and bind to address
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind(('', PORT))
    udpSock.settimeout(5.0)

    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


    try:
        threads.append (threading.Thread(target=keepAliveListener, args=(udpSock, )))
    except:
        print "Nao foi possivel iniciar thread Listener"

    try:
        threads.append( threading.Thread(target=keepAliveSend, args=(udpSock, )))
    except:
        print "Nao foi possivel iniciar thread Sender"

    try:
        threads.append( threading.Thread(target=keepAlivePeers, args=()))
    except:
        print "Nao foi possivel iniciar thread Peer"

    for thread in threads:
        thread.daemon = True
        thread.start()


    for thread in threads:
        thread.join()

    # Close socket
    udpSock.close()
    print 'UDP listener stopped.'

