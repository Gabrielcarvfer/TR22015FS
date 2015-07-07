#!/usr/bin/env python
import os
import hashlib
import pickle
import urllib2

#indexFiles('syncedFiles', file_dict)
def indexFiles(directory, file_dict, local_mac):
    #print 'Indexing...'
    for root, subdirs, files in os.walk(directory):
        #print('--\nroot = ' + root)
        #list_file_path = os.path.join(root, 'my-directory-list.txt')
        #print('list_file_path = ' + list_file_path)

        for filename in files:
            file_path = os.path.join(root, filename)
            #print file_path
            m = hashlib.md5(file_path).digest()
            #print m
            owner_peers = []
            owner_peers.append(local_mac)
            file_dict['%s' % m] = (file_path, owner_peers )

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

def mergeFileDictionaries(local_file_dict, remote_file_dict):
    for file in remote_file_dict:
        if local_file_dict.has_key(file):
            print 'remote file %s already exists here, adding remote peer %s as owner' % (local_file_dict[file][0], remote_file_dict[file][1])
            local_file_dict[file][1].append(remote_file_dict[file][1])
        else:
            print 'remote file %s doesnt exists here, adding to local dictionary' % (remote_file_dict[file][0])
            local_file_dict[file] = remote_file_dict[file]
    return local_file_dict

#receives MAC and IP
def downloadFileRemoteDictionary(k, peer_ip):
    with open('temp/%s.bd' %k, 'wb') as f:
        f.write(urllib2.urlopen('http://' + peer_ip + ':8080/file_dict.bd').read())
        f.close()
    return 'temp/%s.bd' % k

#print 'Files...'
#for files in file_dict:
#    print file_dict[files]


		
