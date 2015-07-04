#!/usr/bin/env python
from websock import websock
from sockthread import UDPServer
import threading

def main():
    peer_dict = {}
    threads = []
    try:
        try:
            threads.append(threading.Thread(target=websock,args=(80,)))
            threads[0].start()
            print 'Started httpserver...'
        except:
            print 'Could not start httpserver'

        try:
            threads.append( threading.Thread(target=UDPServer, args=(peer_dict,)))
            threads[1].start()
            print 'Started udp broadcaster...'
        except:
            print 'Could not start udpserver'

        threads[0].join()
        threads[1].join()


    except KeyboardInterrupt:
        print '^C received, shutting down server'



if __name__ == '__main__':
    main()
		
