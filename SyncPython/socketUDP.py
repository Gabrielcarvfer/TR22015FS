#!/usr/bin/env python

# This code is written by Stephen C Phillips.
# It is in the public domain, so you can do what you like with it
# but a link to http://scphillips.com would be nice.
import time
import socket
import re

host = '' #socket.gethostname()
udp_ip = "255.255.255.255"
udp_port = 54321

def udpsock_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, udp_port))
    print 'Listening to UDP...:', udp_port
    sock.listen(1) # don't queue up any requests
    while True:
        csock, caddr = sock.accept()
        print "Listening message from: " + `caddr`
        req = csock.recv(1024) # get the request, 1kB max
        print req
        # Look in the first line of the request for a move command
        # A move command should be e.g. 'http://server/move?a=90'
        match = re.match('GET /move\?a=(\d+)\sHTTP/1', req)
        if match:
            angle = match.group(1)
            print "ANGLE: " + angle + "\n"
            csock.sendall("Message received\r\n")
        else:
            # If there was no recognised command then return a 404 (page not found)
            print "Returning 404"
            csock.sendall("Error in message\r\n")
        csock.close()
        time.sleep(.100)

def udpsock_broadcaster():

    MESSAGE = "Hello, World!\r\n"

    #print "UDP target IP:", udp_ip
    #print "UDP target port:", udp_port
    #print "message:", MESSAGE

    sockb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockb.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sockb.bind((host, udp_port+1))
    while True:
        sockb.sendto(MESSAGE, (udp_ip, udp_port))
        time.sleep(1.15)
