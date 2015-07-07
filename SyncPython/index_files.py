#!/usr/bin/env python
import os
import hashlib
import pickle
import urllib2
import time

def indexFiles(directory, file_dict, local_mac):
    while True:
        #print 'Indexing...'
        for root, subdirs, files in os.walk(directory):
            #print('--\nroot = ' + root)
            #list_file_path = os.path.join(root, 'my-directory-list.txt')
            #print('list_file_path = ' + list_file_path)

<<<<<<< HEAD
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.sep == '\\':
                file_path = file_path.replace('\\', '/')
            #print file_path
            m = hashlib.md5(file_path).digest()
            #print m
            owner_peers = []
            owner_peers.append(local_mac)
            owner_peers = {}
            owner_peers[local_mac] = 1
            file_dict['%s' % m] = (file_path, owner_peers )
=======
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.sep == '\\':
                    file_path = file_path.replace('\\', '/')
                #print file_path
                m = hashlib.md5(file_path).digest()
                #print m
                owner_peers = []
                owner_peers.append(local_mac)
                owner_peers = {}
                owner_peers[local_mac] = 1
                file_dict['%s' % m] = (file_path, owner_peers )
        time.sleep(5)
>>>>>>> 776b265b166593b6bc442100681c13f21d25f6b8

def dumpDictionaries(file_dict, peer_dict):
    with open('webpage/file_dict.bd', 'w') as handle:
        pickle.dump(file_dict, handle)
        handle.close()
    with open('webpage/peer_dict.bd', 'w') as handle:
        pickle.dump(peer_dict, handle)
        handle.close()

def recoverDictionaries():
    file_dict = readDictionary('webpage/file_dict.bd')
    peer_dict = readDictionary('webpage/peer_dict.bd')
    return(file_dict, peer_dict)

def readDictionary(dictionary_path):
    with open(dictionary_path, 'r') as handle:
        dict = pickle.load(handle)
    return dict

def mergeFileDictionaries(local_file_dict, remote_file_dict, local_mac):
    for file in remote_file_dict:
        if local_file_dict.has_key(file):
            if remote_file_dict[file][1].has_key(local_mac):
                #if file already is registered with local mac, don't do anything
                continue
            else:
                print 'remote file %s already exists here, adding remote peer %s as owner' % (local_file_dict[file][0], remote_file_dict[file][1])
                local_file_dict[file][1].update(remote_file_dict[file][1])
        else:
            print 'remote file %s doesnt exists here, adding to local dictionary' % (remote_file_dict[file][0])
            local_file_dict[file] = remote_file_dict[file]
    return local_file_dict

#receives MAC and IP
def downloadRemoteDictionary(k, peer_ip):
    print peer_ip
    with open('temp/%s.bd' %k, 'wb') as f:
        f.write(urllib2.urlopen('http://' + peer_ip + ':8080/file_dict.bd').read())
        f.close()
    return 'temp/%s.bd' % k

def downloadRemoteFile(file, peer_ip):
    with open('%s' % file, 'wb') as f:
        f.write(urllib2.urlopen('http://' + peer_ip + ':8080' + file ).read())
        f.close()

def syncFilesThread(file_dict, peer_dict, LOCAL_MAC):
    dumpDictionaries(file_dict, peer_dict)

    #(file_dict, peer_dict) = recoverDictionaries()

    while True:
        for files in file_dict:
            print file_dict[files]

        keys = copy_keys(peer_dict)
        for k in keys:
            if LOCAL_MAC == k:
                continue
            else:
                #print peer_dict[k]
                remote_file_dict = readDictionary(downloadRemoteDictionary(k, peer_dict[k]))
                #download all remote files than merge file dictionaries
                for files in remote_file_dict:
                    if remote_file_dict[files][1].has_key(k):
                        continue
                    else:
                        downloadRemoteFile(remote_file_dict[files][0], peer_dict[remote_file_dict[files][1]])
                mergeFileDictionaries(file_dict, remote_file_dict, LOCAL_MAC)
        time.sleep(10)

def copy_keys(object):
    keys = object.keys()
    return keys
#print 'Files...'
#for files in file_dict:
#    print file_dict[files]


		
