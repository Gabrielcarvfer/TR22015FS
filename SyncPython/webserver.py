#!/usr/bin/env python
from websock import websock
from sockthread import UDPServer
from index_files import indexFiles
import threading
import time
import signal
from exchange_files import *

threads = []

def main():

    # workaround to get local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    LOCAL_IP = s.getsockname()[0]
    s.close()

    peer_dict = {}
    file_dict = {}

    try:
        #trying to start http server
        try:
            threads.append(threading.Thread(target=websock,args=(8080,)))
            threads[0].daemon = True
            threads[0].start()
            print 'Started httpserver...'
        except:
            print 'Could not start httpserver'

        #trying to start udp server
        try:
            threads.append( threading.Thread(target=UDPServer, args=(peer_dict, LOCAL_IP, )))
            threads[1].daemon = True
            threads[1].start()
            print 'Started udp broadcaster...'
        except:
            print 'Could not start udpserver'

        #trying to start file server
        try:
            indexFiles('syncedFiles', file_dict)
            pass
        except:
            pass

        while True:
            #for files in file_dict:
            #    print file_dict[files]
            keys = copy_keys(peer_dict)
            for k in keys:
                print peer_dict[k]
            time.sleep(10)

        threads[0].join()
        threads[1].join()


    except KeyboardInterrupt:
        print '^C received, shutting down server'
        import sys
        sys.exit(1)

def copy_keys(object):
    keys = object.keys()
    return keys

if __name__ == '__main__':
    main()
		
