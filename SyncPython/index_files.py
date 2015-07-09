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
                if m in gvar.file_dict:
                    continue
                else:
                    gvar.file_dict.update({m:(file_path, {gvar.mac: (1)})})

        time.sleep(23)

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

def mergeFileDictionaries(remote_mac, remote_file_dict):
    for file in remote_file_dict:
        #check if file is already on dictionary, if its not, then add it
        if file in gvar.file_dict:
            if gvar.mac in gvar.file_dict[file][1]:
                #if file already is registered with local mac, don't do anything
                continue
            else:
                print 'remote file %s already exists here, already added remote peer %s as owner' % (gvar.file_dict[file][0], remote_mac)

                continue
        else:
            print 'remote file %s doesnt exists here, adding to local dictionary' % (remote_file_dict[file][0])
            gvar.file_dict[file] = remote_file_dict[file]

#receives MAC and IP
def downloadRemoteDictionary(k, peer):
   try:
        if peer[1] == 1:
            with open('temp/%s.bd' %k, 'wb') as f:
                #print 'http://' + peer_ip[0] + ':8080/file_dict.bd'
                remote_file = urllib2.urlopen('http://' + peer[0] + ':8080/file_dict.bd')
                f.write(remote_file.read())
                f.close()
                return 'temp/%s.bd' % k
        else:
            print "Remote server is offline\n"
            return 'failed'
   except:
        return 'failed'
        pass


def downloadRemoteFile(file, peer):
    try:
        if peer[1] == 1:
            print 'Downloading remote file http://' + peer[0] + ':8080' + file
            remote_file = urllib2.urlopen('http://' + peer[0] + ':8080' + file)
            with open('webpage/%s' % file, 'wb') as f:
                f.write(remote_file.read())
                f.close()
        else:
            print 'Remote server is offline'
    except:
        pass

def syncFilesThread():
    #recoverDictionaries()
    while True:
        dumpDictionaries()
        #for files in gvar.file_dict:
            #print gvar.file_dict[files]

        #repeat for every known peer
        keys = gvar.peer_dict
        for k in keys:
            #print gvar.mac
            #file already exists in local server
            if (gvar.mac) == k:
                continue
            else:
            #file is only available in remote servers
                #print gvar.peer_dict[k]
                downloadRemoteDictionary(k, gvar.peer_dict[k])
                remote_file_dict = readDictionary('temp/%s.bd' % k)
                #download all remote files without copies than merge file dictionaries
                if remote_file_dict != 'failed':
                    for files in remote_file_dict:
                        #print remote_file_dict[files]
                        #if local server is already on dictionary skip
                        if gvar.mac in remote_file_dict[files][1]:
                            continue
                        else:
                        #if not on marked as file owner
                            file_owners = remote_file_dict[files][1]
                            #check if file has a copy on the network
                            if len(file_owners) >= 2:
                                continue
                            #if not, then copy it to local server
                            else:
                                #remote ip and file
                                #print keys[k][0] + remote_file_dict[files][0]
                                downloadRemoteFile(remote_file_dict[files][0], keys[k][0])
                                gvar.file_dict[files][1].update({k:(1)})
                    mergeFileDictionaries(k, remote_file_dict)
        time.sleep(27)

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
#print 'Files...'
#for files ingvar.file_dict:
#    printgvar.file_dict[files]


		
