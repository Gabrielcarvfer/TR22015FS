#!/usr/bin/env python
from websock import websock
from sockthread import UDPServer
from index_files import indexFiles
import threading

def main():
    peer_dict = {}
    file_dict = {}
    threads = []
    try:
        #trying to start http server
        try:
            threads.append(threading.Thread(target=websock,args=(80,)))
            threads[0].start()
            print 'Started httpserver...'
        except:
            print 'Could not start httpserver'

        #trying to start udp server
        try:
            threads.append( threading.Thread(target=UDPServer, args=(peer_dict,)))
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



        threads[0].join()
        threads[1].join()


    except KeyboardInterrupt:
        print '^C received, shutting down server'



if __name__ == '__main__':
    main()
		
