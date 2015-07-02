#!/usr/bin/env python
#coding=utf-8
import cgi, os
import cgitb; cgitb.enable()

try: # Windows needs stdio set for binary mode.
    import msvcrt
    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
    pass

form = cgi.FieldStorage()

# A nested FieldStorage instance holds the file
username = form.getvalue('login')

# Test if the file was uploaded
if username:
   open('info/user.txt', 'w').write(username)
   message = 'Usuario cadastrado com sucesso'
   
else:
   message = 'Login não efetuado'
 
print """\
Content-Type: text/html\n
<html>
<head><meta http-equiv="refresh" content="1;URL='mainpage.py'" />
</head>
<body>
<p>%s</p>
</body>
</html>
""" % (message,	)
