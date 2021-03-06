#!/usr/bin/env python
from websock import websock
from sockthread import UDPServer, getLocalIP, getSockMac
from index_files import indexFiles, syncFilesThread
import threading
import gvar

threads = []

def main():
    gvar.ip = getLocalIP()
    gvar.mac = getSockMac()

    try:
        #trying to start http server
        try:
            threads.append(threading.Thread(target=websock,args=(8080,'')))
            threads[0].daemon = True
            threads[0].start()
            print 'Started httpserver...'
        except:
            print 'Could not start httpserver'

        #trying to start udp server
        try:
            threads.append( threading.Thread(target=UDPServer, args=()))
            threads[1].daemon = True
            threads[1].start()
            print 'Started udp broadcaster...'
        except:
            print 'Could not start udpserver'

        #trying to start file indexing server
        try:
            threads.append( threading.Thread(target=indexFiles, args=('webpage/syncedFiles', )))
            threads[2].daemon = True
            threads[2].start()
            pass
        except:
            pass

        #trying to start file sync server
        try:
            threads.append( threading.Thread(target=syncFilesThread, args=( )))
            threads[3].daemon = True
            threads[3].start()
            pass
        except:
            pass

        threads[0].join()
        threads[1].join()
        threads[2].join()
        threads[3].join()


    except KeyboardInterrupt:
        print '^C received, shutting down server'
        import sys
        sys.exit(1)



if __name__ == '__main__':
    main()
		
