#!/usr/bin/env python
import os
import hashlib
import pickle
import urllib2
import time
import gvar

def indexFiles(directory):
    while True:
        for root, subdirs, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.sep == '\\':
                    file_path = file_path.replace('\\', '/')
                file_path = file_path.replace('webpage', '')
                #print file_path
                m = hashlib.md5(file_path).digest()
                #print m
                owner_peers = {}
                owner_peers[gvar.mac] = 1
                gvar.file_dict['%s' % m] = (file_path, owner_peers )

        time.sleep(2)

def dumpDictionaries():
    try:
        with open('webpage/file_dict.bd', 'wb') as handle:
            file_dict = gvar.file_dict
            pickle.dump(file_dict, handle)
            handle.close()
        with open('webpage/peer_dict.bd', 'wb') as handle:
            peer_dict = gvar.file_dict
            pickle.dump(peer_dict, handle)
            handle.close()
    except:
        pass

def recoverDictionaries():
    gvar.file_dict = readDictionary('webpage/file_dict.bd')
    gvar.peer_dict = readDictionary('webpage/peer_dict.bd')
    return()

def readDictionary(dictionary_path):
    try:
        with open(dictionary_path, 'rb') as handle:
            dict = pickle.load(handle)
        return dict
    except:
        pass

def mergeFileDictionaries(remote_file_dict):
    for file in remote_file_dict:
        if gvar.file_dict.has_key(file):
            if remote_file_dict[file][1].has_key(gvar.mac):
                #if file already is registered with local mac, don't do anything
                continue
            else:
                print 'remote file %s already exists here, adding remote peer %s as owner' % (gvar.file_dict[file][0], remote_file_dict[file][1])
                gvar.file_dict[file][1].update(remote_file_dict[file][1])
        else:
            print 'remote file %s doesnt exists here, adding to local dictionary' % (remote_file_dict[file][0])
            gvar.file_dict[file] = remote_file_dict[file]

#receives MAC and IP
def downloadRemoteDictionary(k, peer_ip):
    #try:
        print peer_ip
        with open('temp/%s.bd' %k, 'wb') as f:
            #print 'http://' + peer_ip + ':8080/file_dict.bd'
            f.write(urllib2.urlopen('http://' + peer_ip + ':8080/file_dict.bd').read())
            f.close()
        return 'temp/%s.bd' % k
    #except:
    #    pass
    #    return 'f'

def downloadRemoteFile(file, peer_ip):
    try:
        with open('webpage/%s' % file, 'wb') as f:
            print 'http://' + peer_ip + ':8080' + file
            f.write(urllib2.urlopen('http://' + peer_ip + ':8080' + file ).read())
            f.close()
    except:
        pass

def syncFilesThread():
    #recoverDictionaries()
    while True:
        dumpDictionaries()
        local_peers = gvar.peer_dict
        #for files in gvar.file_dict:
            #print gvar.file_dict[files]

        keys = gvar.peer_dict
        for k in keys:
            #print gvar.mac
            if ('%s' % gvar.mac) == k:
                continue
            else:
                #print gvar.peer_dict[k]
                downloadRemoteDictionary(k, gvar.peer_dict[k])
                remote_file_dict = readDictionary('temp/%s.bd' % k)
                #download all remote files than merge file dictionaries
                if remote_file_dict != 'f':
                    for files in remote_file_dict:
                        print remote_file_dict[files]
                        if num(gvar.mac) in remote_file_dict[files][1]:
                            continue
                        else:
                            mac = (remote_file_dict[files][1].keys()[0])
                            remote_ip = ''

                            for peer in local_peers:
                                  mmac = ('%s' % mac)
                                  if peer[0] in mmac:
                                      remote_ip = local_peers[mmac]
                                      break

                                #local_peers.keys()
                                #remote_ip = local_peers[mac]

                            print remote_ip
                            print remote_file_dict[files][0]
                            downloadRemoteFile(remote_file_dict[files][0], remote_ip)
                    mergeFileDictionaries(remote_file_dict)
        time.sleep(30)

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
#print 'Files...'
#for files ingvar.file_dict:
#    printgvar.file_dict[files]


		
