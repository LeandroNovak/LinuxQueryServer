#!/usr/bin/env python
# webserver.py
# deve ser armazenado na pasta /usr/lib/cgi-bin/ da maquina virtual

import cgi
import cgitb

cgitb.enable(display=0, logdir="~/logs")
args = cgi.FieldStorage()

print("Content-Type: text/html;charset=utf-8\r\n")
print("<head><title>Trabalho 1 de Redes</title></head>")