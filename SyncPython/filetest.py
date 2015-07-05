#!/usr/bin/env python
from index_files import indexFiles
import os
import hashlib

file_dict = {}


print 'Indexing...'
#indexFiles('syncedFiles', file_dict)
directory = 'syncedFiles'

import os

for root, subdirs, files in os.walk(directory):
    #print('--\nroot = ' + root)
    list_file_path = os.path.join(root, 'my-directory-list.txt')
    #print('list_file_path = ' + list_file_path)

    for filename in files:
        file_path = os.path.join(root, filename)
        #print file_path
        m = hashlib.md5(file_path).digest()
        #print m
        file_dict['%s' % m] = file_path

print 'Files...'
for files in file_dict:
    print file_dict[files]


		
