import socket
import sys


s = socket.socket()
s.bind(('',9999))
s.listen(10) # Acepta hasta 10 conexiones entrantes.
sc, address = s.accept()

print address

f = open('recvfile/file_recv.txt','wb') #open in binary

l = sc.recv(1024)
while (l):
    f.write(l)
    l = sc.recv(1024)
f.close()


sc.close()
s.close()