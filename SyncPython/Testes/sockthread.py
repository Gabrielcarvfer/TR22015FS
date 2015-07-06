#!/usr/bin/python

import thread
import time
import socket
import re
import threading
from uuid import getnode as get_mac


# Porta UDP para broadcast do keep alive
PORT = 54321
BROADCAST_IP = '255.255.255.255'
threads = []
#HOST_IP = ''


def keepAliveListener(conn, LOCAL_IP, dict):
    while 1:
        # Receive messages
        while True:
            try:
                data, addr = conn.recvfrom(1028)
                #if (addr[0] != LOCAL_IP):
                # debug printing
                print "From addr: '%s', msg: '%s'" % (addr[0], data)

                # filter source MAC address to match.group(1) and IP address to match.group(2)
                match = re.match('SYNCFILES_MAC_(\d+)_IP_(.*$)', data)

                # debug printing
                #print match.group(1)
                #print match.group(2)

                # parse data into peer dictionary
                #if dict.has_key(match.group(1)):
                #TODO: reset peer timer
                #    continue

                if dict.has_key(match.group(1)):
                    if dict[match.group(1)] == match.group(2):
                        continue
                    else:
                        dict[match.group(1)] = match.group(2)
                    continue
                else:
                    dict[match.group(1)] = match.group(2)
                    #print 'New peer:' + dict[match.group(1)]
                    #TODO:set new peer timer
                    continue



                    #else:
                    # print 'Message received was sent by myself'
                    # continue
            except:
                print "timeout"
time.sleep(0.010)


def keepAliveSend(conn, LOCAL_IP):
    while True:
        mac = get_mac()
        conn.sendto(('SYNCFILES_MAC_%s_IP_%s' % (mac, LOCAL_IP)), (BROADCAST_IP, PORT))
        time.sleep(1)


def UDPServer(dict, LOCAL_IP):

    # Create socket and bind to address
    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind((LOCAL_IP, PORT))
    udpSock.settimeout(5.0)

    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


    try:
        threads.append (threading.Thread(target=keepAliveListener, args=(udpSock, LOCAL_IP, dict,)))
        # thread.start_new_thread( keepAliveListener, (udpSock, LOCAL_IP, dict, ) )
    except:
        print "Nao foi possivel iniciar thread Listener"

    try:
        threads.append( threading.Thread(target=keepAliveSend, args=(udpSock, LOCAL_IP,)))
        # thread.start_new_thread( keepAliveSend, (udpSock, LOCAL_IP,) )
    except:
        print "Nao foi possivel iniciar thread Sender"

    # while 1:
    #    time.sleep(100)
    #    pass
    for thread in threads:
        thread.daemon = True
        thread.start()


    for thread in threads:
        thread.join()

    # Close socket
    udpSock.close()
    print 'UDP listener stopped.'

