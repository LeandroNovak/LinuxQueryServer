#!/usr/bin/env python
import cgi
import cgitb
from backend import *

cgitb.enable()
form = cgi.FieldStorage()

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
for i in range(1, 4):
	cmd_list = []
	# ps command
	if form.has_key("maq" + str(i) + "_ps"):
		if form.has_key("maq" + str(i) + "-ps"):
			cmd_list.append(("ps", str(form["maq" + str(i) + "-ps"].value)))
		else:
			cmd_list.append(("ps", ""))
	# df command
	if form.has_key("maq" + str(i) + "_df"):
		if form.has_key("maq" + str(i) + "-df"):
			cmd_list.append(("df", str(form["maq" + str(i) + "-df"].value)))
		else:
			cmd_list.append(("df", ""))
	# finger command
	if form.has_key("maq" + str(i) + "_finger"):
		if form.has_key("maq" + str(i) + "-finger"):
			cmd_list.append(("finger", str(form["maq" + str(i) + "-finger"].value)))	
		else:
			cmd_list.append(("finger", ""))
	# uptime command
	if form.has_key("maq" + str(i) + "_uptime"):
		if form.has_key("maq" + str(i) + "-uptime"):
			cmd_list.append(("uptime", str(form["maq" + str(i) + "-uptime"].value)))
		else:
			cmd_list.append(("uptime", ""))
	# sends commands to backend and receives result
	result = execute(i, cmd_list)
	# prints the result
	for j in range(len(result)):
		print(result[j].replace("\n", "<br>"))
		print("<br><br>")

