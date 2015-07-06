#!/usr/bin/python

import socket  # Networking support
import signal  # Signal support (server shutdown on signal receive)
import time    # Current time
import os.path
import shutil
import re

class websock:
    """ Class describing a simple HTTP server objects."""

    def __init__(self, port = 8080):
        """ Constructor """
        self.host = ''   # <-- works on all avaivable network interfaces
        self.port = port
        self.www_dir = 'webpage' # Directory where webpage files are stored
	#self.www_dir = ''        
	self.activate_server()
        self._wait_for_connections()


    def activate_server(self):
        """ Attempts to aquire the socket and launch the server """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: # user provided in the __init__() port may be unavaivable
            print("Launching HTTP server on ", self.host, ":",self.port)
            self.socket.bind((self.host, self.port))

        except Exception as e:
            print ("Warning: Could not aquite port:",self.port,"\n")
            print ("I will try a higher port")
            # store to user provideed port locally for later (in case 8080 fails)
            user_port = self.port
            self.port = 8080

            try:
                print("Launching HTTP server on ", self.host, ":",self.port)
                self.socket.bind((self.host, self.port))

            except Exception as e:
                print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
                print("Try running the Server in a privileged user mode.")
                self.shutdown()
                import sys
                sys.exit(1)

        print ("Server successfully acquired the socket with port:", self.port)
        print ("Press Ctrl+C to shut down the server and exit.")
        self._wait_for_connections()

    def shutdown(self):
        """ Shut down the server """
        try:
            print("Shutting down the server")
            self.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            print("Warning: could not shut down the socket. Maybe it was already closed?",e)


    def _gen_headers(self,  code):
        """ Generates HTTP response Headers. Ommits the first line! """

        # determine response code
        h = ''
        if (code == 200):
            h = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
            h = 'HTTP/1.1 404 Not Found\n'

        # write further headers
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        h += 'Date: ' + current_date +'\n'
        h += 'Server: Simple-Python-HTTP-Server\n'
        h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

        return h

    def _wait_for_connections(self):
        """ Main loop awaiting connections """
        while True:
            print ("Awaiting New connection")
            self.socket.listen(3) # maximum number of queued connections

            conn, addr = self.socket.accept()
            # conn - socket to client
            # addr - clients address

            print("Got connection from:", addr)

            data = conn.recv(1024) #receive data from client
            string = bytes.decode(data) #decode it to string

            #determine request method  (HEAD and GET are supported)
            request_method = string.split(' ')[0]
            print ("Method: ", request_method)
            print ("Request body: ", string)

            #if string[0:3] == 'GET':
            if (request_method == 'GET') | (request_method == 'HEAD'):
                #file_requested = string[4:]

                # split on space "GET /file.html" -into-> ('GET','file.html',...)
                file_requested = string.split(' ')
                file_requested = file_requested[1] # get 2nd element

                #Check for URL arguments. Disregard them
                file_requested = file_requested.split('?')[0]  # disregard anything after '?'

                if (file_requested == '/'):  # in case no file is specified by the browser
                    file_requested = '/index.html' # load index.html by default


                file_requested = self.www_dir + file_requested
                print ("Serving web page [",file_requested,"]")

                ## Load file content
                try:
                    file_handler = open(file_requested,'rb')
                    if (request_method == 'GET'):  #only read the file when GET
                        response_content = file_handler.read() # read file content
                    file_handler.close()

                    response_headers = self._gen_headers( 200)

                except Exception as e: #in case file was not found, generate 404 page
                    print ("Warning, file not found. Serving response code 404\n", e)
                    response_headers = self._gen_headers( 404)

                    if (request_method == 'GET'):
                        response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"


                server_response =  response_headers.encode() # return headers for GET and HEAD
                if (request_method == 'GET'):
                    server_response +=  response_content  # return additional conten for GET only


                conn.send(server_response)
                print ("Closing connection with client")
                conn.close()

            if(request_method == 'POST'):
                print "Solicitacao de post"
                file_requested = string.split(' ')
                file_requested = file_requested[1]
                last_line = string.split(" ")[-1:]
                
                parameter = last_line[-1].split('\n')
                print parameter[-1]
                some_parameters = parameter[-1].split('=')
                tipo = some_parameters[0]
                print tipo
                
                if tipo == "login":
                    login = some_parameters[1]
                
                if tipo == "dir":
                    new_dir = some_parameters[2]
                    #print new_dir
                    father_dir = some_parameters[1].split('&')
                    father_dir = father_dir[0]
                    father_dir = father_dir.replace("%2F", "/");
                    father_dir = father_dir.replace("%5C", "/");
                    #print father_dir

                    re.sub(r'\W+', '', new_dir)
                    #father_dir = filter(str.isalnum, father_dir)
                    #new_dir = filter(str.isalnum, new_dir)
                    p = os.path.dirname( father_dir + '/' + new_dir+ '/')
		    print father_dir
		    print new_dir
                    if not os.path.exists(p):
                       os.makedirs(p)
                   #print "Erro"
                   #message = 'Novo diretorio cadastrado com sucesso'

                if tipo == "delete_dir":
                    delete_dir = some_parameters[1]
                    delete_dir = delete_dir.replace("%2F", "/")
                    delete_dir = delete_dir.replace("%5C", "/")
                    #print delete_dir
                    shutil.rmtree(delete_dir)

                if tipo == "fileDir":
                    new_file = some_parameters[2]
                    file_dir = some_parameters[1].split('&')
                    file_dir = file_dir[0]
                    file_dir = file_dir.replace("%2F", "/")
                    file_dir = file_dir.replace("%5C", "/")
                    new_file = new_file.replace("%2F", "/")
                    new_file = new_file.replace("%5C", "/")
                    new_file = new_file.replace("%3A", ":")
                    print file_dir
                    print new_file
                    if os.path.isfile(new_file):
                        shutil.copy2(new_file,file_dir)

                if tipo == 'file_delete':
                    file_address = some_parameters[1]
                    file_address = file_address.replace("%2F", "/")
                    file_address = file_address.replace("%5C", "/")
                    file_address = file_address.replace("%3A", ":")
                    if os.path.isfile(file_address):
                        os.remove(file_address)
                    print file_address
                    
                file_requested = "Mainpage"
                file_requested = self.www_dir + file_requested
                print ("Serving web page [",file_requested,"]")
                response_content = mainpage(login)
                response_headers = self._gen_headers( 200)
                server_response =  response_headers.encode()
                server_response +=  response_content


                conn.send(server_response)
                print ("Closing connection with client")
                conn.close()

            else:
                print("Unknown HTTP request method:", request_method)


def mainpage( str ):
    header =  """<!DOCTYPE html> <html> <head>Bem vindo, %s!</head>""" %(str)
    tree = '<ul>'

    for path, dirs, files in os.walk('./webpage/syncedFiles'):
        lining = path.count('/')
        for x in range (0,lining-1):
            tree += '<ul>'
        tree +='<li>'+ os.path.basename(path) 
        tree +='<ul>'
        for f in files:
            tree += '<li><a href=http://localhost:8080/'+os.path.basename(path)+'/'+f+' target="_blank">'+f+'</a></li>'
        tree += '</li>'
        for x in range (0,lining):
            tree+= '</ul>'
    tree+= '</ul>'

    body = """ <body> <div> <p>Criar novo diretorio</p>
<form  method="POST" ">
<p>Nome do pai do novo diretorio:<select name="dir">"""
    for path, dirs, files in os.walk('./webpage/syncedFiles'):
        body +='<option value='+ path + '>' + os.path.basename(path) + '</option>'
    body += """\  
    </select></p>
    <p>Nome do novo diretorio:<input type="text"name="dirName"></p>
    <input type="submit" value="Submit">
    </form>
    </div>
    <div>
    <p>Deletar diretorio</p>
    <form  method="POST" ">
    <p>Diretorio a ser deletado(e todos os arquivos):<select name="delete_dir">"""
    for path, dirs, files in os.walk('./webpage/syncedFiles'):
        if path != './webpage/syncedFiles':
            body +='<option value='+ path + '>' + os.path.basename(path) + '</option>'
    body += """\  
    </select></p>
    <input type="submit" value="Submit">
    </form>
    </div>	<div>
    
    <p>Adicionar arquivo</p>
    <form " method="post" >
    <p>Diretorio onde o arquivo vai ser alocado:</p>
    <select name="fileDir">
    """
    for path, dirs, files in os.walk('./webpage/syncedFiles'):
        body +='<option value='+ path + '>' + os.path.basename(path) + '</option>'
    body +=  """\
    </select>
    </p>     
    <input type="text" name="upfile" /> 
            <input type="submit" value="Send" />
            </form>
            </div>


    <div> <p>Deletar arquivo</p>
    <form  method="POST" ">
    <p>Selecione o arquivo a ser deletado:<select name="file_delete">"""
    
    for path, dirs, files in os.walk('./webpage/syncedFiles'):
        for f in files:
            body +='<option value='+ os.path.abspath(path)+'/'+f+ '>' + os.path.abspath(path)+'/'+f + '</option>'


    body += """\  
    </select></p>
       <input type="submit" value="Submit">
    </form>
    </div>
    <div>
    <p>Deletar diretorio</p>
    <form  method="POST" ">
    <p>Diretorio a ser deletado(e todos os arquivos):<select name="delete_dir">"""
    for path, dirs, files in os.walk('./webpage/syncedFiles'):
        if path != './webpage/syncedFiles':
            body +='<option value='+ path + '>' + os.path.basename(path) + '</option>'
    body += """\  
    </select></p>
    <input type="submit" value="Submit">
    </form>
    </div>

     </body>
    </html>

    """
# <form enctype="multipart/form-data" " method="post" >
    return header+tree+body
    

def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown() #shut down the server
    import sys
    sys.exit(1)
    

