#!/usr/bin/env python
#coding=utf-8
import cgi, os
import cgitb; cgitb.enable()
import os.path
import re
# Function declaration
 
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
   #fatherDir = filter(str.isalnum, fatherDir)
   newDirName = filter(str.isalnum, newDirName)
   p = os.path.dirname( fatherDir + '/' + newDirName+ '/')
   if not os.path.exists(p):
       os.makedirs(p)
   print "Erro"
   message = 'Novo diretorio cadastrado com sucesso'

if fileDir and fileName:
    fileDir = filter(str.isalnum, fileDir)
    fileName = filter(str.isalnum, fileName)
    open('info/arquivos.txt','a').write(fileDir + ' ' +fileName + '\n')
    open('info/arquivos.txt','a').write(fileDir + ' ' +fileName + '\n')
    open('info/'+fileDir+'.txt','a').write('file '+fileName + ' \n')

fh = open("info/user.txt", "r")
userName = fh.read()
fh.close()

print """\
<!DOCTYPE html>

<html>
 
<head>Bem vindo, %s!</head>
""" %(userName)

print '<ul>'
for path, dirs, files in os.walk('.\info'):
    lining = path.count('\\')
    for x in range (0,lining-1):
        print '<ul>'
    print '<li>'+ os.path.basename(path) 
    print '<ul>'
    for f in files:
        print '<li>'+f+'</li>'
    print '</li>'
    for x in range (0,lining):
        print '</ul>'
print '</ul>'

print """\
   <body>

<div>
<p>Criar novo diretorio</p>
<form  method="POST" action="../cgi-bin/mainpage.py">
<p>Nome do pai do novo diretorio:
<select name="dir">
"""


for path, dirs, files in os.walk('./info'):
    print '<option value='+ path + '>' + os.path.basename(path) + '</option>'

print """\  
</select></p>
<p>Nome do novo diretorio:<input type="text"name="dirName"></p>
<input type="submit" value="Submit">
</form>
</div>

    
	<div>
<p>Adicionar arquivo</p>


<form enctype="multipart/form-data" action="../cgi-bin/upload_file.py" method="post">
	
<p>Diretorio onde o arquivo vai ser alocado:</p>
<select name="fileDir">


"""
for path, dirs, files in os.walk('./info'):
    print '<option value='+ path + '>' + os.path.basename(path) + '</option>'

print """\
</select>
</p>

	
<input type="file" name="upfile" /> 
	
	<input type="submit" value="Send" />
	</form>

	</div>

  

 </body>



</html>

"""
