#!/usr/bin/env python
#coding=utf-8
import cgi, os
import cgitb; cgitb.enable()
import os.path
 
try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

# A nested FieldStorage instance holds the file
fatherDir = form.getvalue('dir')
newDirName = form.getvalue('dirName')
fileDir = form.getvalue('fileDir')
fileName = form.getvalue('fileName')

# Test if the file was uploaded
if fatherDir and newDirName:
   open('info/dir.txt', 'a').write(fatherDir + ' ' + newDirName + '\n')
   message = 'Novo diretorio cadastrado com sucesso'

if fileDir and fileName:
    open('info/arquivos.txt','a').write(fileDir + ' ' +fileName + '\n')

fh = open("info/user.txt", "r")
userName = fh.read()
fh.close()

print """\
<!DOCTYPE html>

<html>
 
<head>Bem vindo, %s!</head>
""" %(userName)

print """\
   <body>

<div>
<p>Criar novo diretorio</p>
<form  method="POST" action="../cgi-bin/mainpage.py">
<p>Nome do pai do novo diretorio:
<select name="dir">
<option value="Arquivos">Arquivos</option>
"""
if os.path.isfile("info/dir.txt"):
    sonDir = ""
    myfile = open("info/dir.txt", "r")
    for line in myfile:
        for char in line:
            if char != " ":
                sonDir += char
            else:
                dadDir = sonDir
                sonDir = ""
            #newDir = myfile.read()
        print """\
        <option value="%s">%s</option>
        """ %(sonDir, sonDir)
    fh.close()

print """\  
</select></p>
<p>Nome do novo diretorio:<input type="text"name="dirName"></p>
<input type="submit" value="Submit">
</form>
</div>

    
	<div>
<p>Adicionar arquivo</p>

<form  method="POST" action="../cgi-bin/mainpage.py">

<p>Diretorio onde o arquivo vai ser alocado:</p>
<select name="fileDir">
<option value="Arquivos">Arquivos</option>

"""

if os.path.isfile("info/dir.txt"):
    sonDir = ""
    myfile = open("info/dir.txt", "r")
    for line in myfile:
        for char in line:
            if char != " ":
                sonDir += char
            else:
                dadDir = sonDir
                sonDir = ""
            #newDir = myfile.read()
        print """\
        <option value="%s">%s</option>
        """ %(sonDir, sonDir)
    fh.close()

print """\
</select>
</p>

	<p>Escolha o arquivo:<input type="file" name="fileName" size="chars">
	</p>

	<input type="submit" value="Send">
	</p>
	</form>
	</div>

  

 </body>



</html>

"""
