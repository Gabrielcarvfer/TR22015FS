#!/usr/bin/env python
from websock import websock
from sockthread import UDPServer, getLocalIP, getSockMac
from index_files import indexFiles, dumpDictionaries, recoverDictionaries, mergeFileDictionaries, readDictionary, downloadFileRemoteDictionary
import threading
import time
threads = []

def main():
    LOCAL_IP = getLocalIP()
    LOCAL_MAC = getSockMac()
    peer_dict = {}
    file_dict = {}

    try:
        #trying to start http server
        try:
            threads.append(threading.Thread(target=websock,args=(8080,LOCAL_IP)))
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
            indexFiles('webpage/syncedFiles', file_dict, LOCAL_MAC)
            pass
        except:
            pass

        dumpDictionaries(file_dict, peer_dict)

        (file_dict, peer_dict) = recoverDictionaries()

        while True:
            #for files in file_dict:
                #print file_dict[files]

            keys = copy_keys(peer_dict)
            for k in keys:
                if LOCAL_MAC == k:
                    continue
                else:
                    print peer_dict[k]
                    remote_file_dict = readDictionary(downloadFileRemoteDictionary(k, peer_dict[k]))
                    mergeFileDictionaries(file_dict, remote_file_dict)
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
		
