#!/usr/bin/python

import socket
import sys
import os
from time import sleep

def recv_file(file_path,filename, PORT):
    s = socket.socket()
    s.bind(('',PORT))
    s.listen(10)
    sc, address = s.accept()
    print "receiving file from: " + str(address)
    f = open(file_path+'/'+filename,'wb') #open in binary
    l = sc.recv(1024)
    while (l):
        f.write(l)
        l = sc.recv(1024)
    f.close()

    sc.close()
    s.close()


def send_file(file_path, destAddr):

    s = socket.socket()
    s.connect((destAddr,9999))

    f=open (file_path, "rb") 
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)

    s.close()

def compara_listas(lista1, lista2):

    """ 
        lista1: lista na memoria
        lista2: lista dos arquivos na pasta
        
        3 casos: 
            1.se listas forem do mesmo tamanho verifica as diferencas
                se tem arquivo na memoria e nao tem na pasta 
                    nao tem problema
                se tem arquivo na pasta e nao tem na memoria
                    diz qual eh
            2.se lista na memoria for menor, precisa adicionar arquivos
            3.se lista na memoria for maior 
                deleta arquivo da memoria

        retorna lista com primeiro elemento indicando qual caso e o resto as diferencas
    """

    igual = 0
    listadif = [0]*len(lista2)

    if len(lista1) <= len(lista2):    
        for i in range(0, len(lista2)):
            for j in range(0, len(lista1)):
                if(lista2[i] == lista1[j]):
                    igual=igual+1
                    break
            if igual==0:
                listadif[i] = 1
            igual = 0
    return listadif

def gen2filelist(fileFolderName):
    fileList = []
    for root, subdir, files in os.walk(fileFolderName):
        for filename in files:
            fileList.append(filename)
    return fileList

def verifica_arquivos_novos(meuip,file_dict, peer_dict, fileFolderName, PORT):
    while 1:
        print file_dict[meuip]
        listaPasta = gen2filelist(fileFolderName)
        listaRes = compara_listas( file_dict[meuip] , listaPasta )

        if sum(listaRes) != 0: # tem diferencas
            for i in range(0, len(listaPasta)):
                if listaRes[i] == 1:
                    print listaPasta[i] + " eh novo!\n"
                    # pra cada ip
                    for key in peer_dict:
                        if peer_dict[key] != meuip:
                            # manda uma mensagem pra dizer que qr mandar um arquivo e espera resposta
                            sock = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM) # UDP
                            sock.sendto("TROCA-"+str(meuip), ( str(peer_dict[key]), PORT ) )

                            while (data != '') and (protocolo != 'TROCAOK'):
                                udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                                udpSock.bind(('', PORT))
                                
                                udpSock.settimeout(5.0)
                                data, addr = sock.recvfrom(1024)
                                protocolo, destAddr = data.split('-')

                        # manda o arquivo
                        #def send_file(file_path, destAddr):
                        send_file(listaPasta[i], destAddr)

        file_dict[meuip] = listaPasta
        sleep(1)

def recebe_arquivo_novo(PORT,meuip,path):
    while 1:
        data = ''
        protocolo = ''
        arqName = ''
        # espera requisicao de arquivo
        while (data != '') and (protocolo != 'TROCA'):
            udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpSock.bind(('', PORT))
            
            udpSock.settimeout(5.0)
            data, addr = sock.recvfrom(1024)
            protocolo, hostaddr = data.split('-')

        if protocolo == 'TROCA':
            # responde ok
            sock = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM) # UDP
            sock.sendto("TROCAOK-"+meuip, (hostaddr, PORT))


            # abre conexao tcp para receber arquivo
            recv_file(path, data, PORT)
