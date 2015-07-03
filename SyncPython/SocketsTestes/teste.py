#!/usr/bin/python

import threading
import thread
import time
import socket
import sys


msgNovoNaArea = 'SouNovoNaArea'

ID = 0


def criaLista():
    pass

def recebeResposta(conn):
    try:
        data, addr = conn.recvfrom(1028)
        if data == msgNovoNaArea:
            recebeResposta(conn)
        # senao cria conexao com servidor TCP
        global ID = 0
    except:
        # set ID = 1
        global ID = 1
        print "UDP timeout sou o primeiro"


# Porta UDP para broadcast do keep alive
if(len(sys.argv) > 1):
    PORT = sys.argv[1]
else:
    PORT = 50000

# Create socket and bind to address
udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSock.bind(('', PORT))
udpSock.settimeout(5.0)
udpSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
udpSock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)

# Manda o broadcast de entrada na rede
udpSock.sendto(msgNovoNaArea, ('255.255.255.255', PORT))
time.sleep(1)

# Verifica resposta da rede
recebeResposta(udpSock)

udpSock.close()

if(ID==1):
    
    pass
    # cria dados na tabela

else:


    pass
    # se atualiza pegando lista de informacoes




# cria thread para criar conexoes
# com a lista cria conexao para tod


# cria thread para keep alive

print "chegou aki"