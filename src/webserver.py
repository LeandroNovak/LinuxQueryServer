#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()
form = cgi.FieldStorage()

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
'''
print("<br><br>")
print(form)
print("<br><br>")
'''
cmd_list = []

for i in range(1, 4):
	#:print("<hd1>Maquina " + str(i) + "</h1><br>")

	if form.has_key("maq" + str(i) + "_ps"):
		if form.has_key("maq" + str(i) + "-ps"):
			cmd_list.append(("maq" + str(i), "ps", str(form["maq" + str(i) + "-ps"].value)))
	if form.has_key("maq" + str(i) + "_df"):
		if form.has_key("maq" + str(i) + "-df"):
			cmd_list.append(("maq" + str(i), "df", str(form["maq" + str(i) + "-df"].value)))
	if form.has_key("maq" + str(i) + "_finger"):
		if form.has_key("maq" + str(i) + "-finger"):
			cmd_list.append(("maq" + str(i), "finger", str(form["maq" + str(i) + "-finger"].value)))
	if form.has_key("maq" + str(i) + "_uptime"):
		if form.has_key("maq" + str(i) + "-uptime"):
			cmd_list.append(("maq" + str(i), "uptime", str(form["maq" + str(i) + "-uptime"].value)))

print("Commands:<br>")
for j in cmd_list:
	print(str(j) + "<br>")
