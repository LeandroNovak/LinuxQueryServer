#!/usr/bin/env python
from threading import Thread
from socket import *
import subprocess
import struct
import sys
import io


def generateChecksum(data):
	pol = 0xCAFE
	crc = 0XFFFF
	for i in range(0, len(data)):
		crc ^= data[i]
		data[i] += data[i]
		for j in range(0, 8):
			if ((crc & 0x001) > 0):
				crc = (crc >> 1) ^ pol
			else:
				crc = (crc >> 1)
	return ((crc & 0xFFFF) + (crc >> 16))


def verifyChecksum(header, crc):
	return (generateChecksum(header) == crc)


class RunCommands(Thread):
	def __init__(self):
		Thread.__init__(self)
	

	def setSocket(self, socket):
		self.socket = socket


	def run(self):
		# receives package from socket
		package = io.BytesIO(self.socket.recv(60))
		package.seek(0)

		# reads header content
		header = struct.unpack("!BBHHHBBHII", package.read(20))
		verihl = int(header[0])
		tos = int(header[1])
		tln = int(header[2])
		idf = int(header[3])
		flgffo = int(header[4])
		ttl = int(header[5])
		ptc = int(header[6])
		chk = int(header[7])
		src = int(header[8])
		dst = int(header[9])
		sizeOptions = (((verihl & int('0b00001111', 2)) - 5) * 4)
		options = "".join(struct.unpack("s" * sizeOptions, package.read()))

		# creates a header for checksum
		headerCheck = []
		headerCheck.append(verihl)
		headerCheck.append(tos)
		headerCheck.append(tln)
		headerCheck.append(idf)
		headerCheck.append(flgffo)
		headerCheck.append(ttl)
		headerCheck.append(ptc)
		headerCheck.append(int(0))
		headerCheck.append(src)
		headerCheck.append(dst)

		# removes padding and eol from options
		arguments = ""
		for i in options:
			if (i == '\n'):
				break
			headerCheck.append(int(ord(i)))
			arguments = arguments + str(i)

		# verifies which command should be executed
		if (ptc == 0):
			command = "ps"
		elif (ptc == 1):
			command = "df"
		elif (ptc == 2):
			command = "finger"
		elif (ptc == 3):
			command = "uptime"

		# checks the checksum and executes the command
		result = ""
		if (verifyChecksum(headerCheck, chk) == True):
			try:
				result = subprocess.check_output([command, arguments])
			except subprocess.CalledProcessError as e:
				result = str(e) 
		else:
			result = "Error: The package may be corrupted"
		
		# calculates the size of the output
		resultSize = len(result) // 4
		if ((len(result) % 4) > 0):
			resultSize = resultSize + 1

		# creates a new header over the old one
		headerCheck[2] = ((resultSize * 4) + 20)
		headerCheck[4] = (7 << 13)
		headerCheck[5] = headerCheck[5] - 1
		temp = headerCheck[8]
		headerCheck[8] = headerCheck[9]
		headerCheck[9] = temp

		# calculates response's checksum
		chk = generateChecksum(headerCheck)
		headerCheck[7] = chk

		# creates the package
		package = io.BytesIO()
		package.write(struct.pack('!B', header[0]))
		package.write(struct.pack('!B', header[1]))
		package.write(struct.pack('!H', header[2]))
		package.write(struct.pack('!H', header[3]))
		package.write(struct.pack('!H', header[4]))
		package.write(struct.pack('!B', header[5]))
		package.write(struct.pack('!B', header[6]))
		package.write(struct.pack('!H', header[7]))
		package.write(struct.pack('!I', header[8]))
		package.write(struct.pack('!I', header[9]))
		package.write(result)
		package.seek(0)

		# sends the package to the client
		self.socket.send(package.read())

		# closes connection
		self.socket.close()


def main():
	if ((len(sys.argv) == 3) and (sys.argv[1] == "--port")):
		port = int(sys.argv[2])
		print("Trying to connect to port " + str(port))

		# creates the socket and waits for up to 8 connections
		server = socket(AF_INET, SOCK_STREAM)
		server.bind(("", port))
		server.listen(8)
		
		while(True):
			connection, address = server.accept()
			run = RunCommands()
			run.setSocket(connection)
			run.start()
		
		server.close()
	else:
		print("Uso daemon.py --port PORT_NUMBER")


if __name__ == "__main__":
	main()
