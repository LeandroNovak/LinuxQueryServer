#!/usr/bin/env python
from socket import *
import struct
import io


def generateChecksum(data):
	pol = 0xCAFE
	crc = 0xFFFF
	for i in range(0, len(data)):
		crc ^= data[i]
		data[i] += data[i]
		for j in range(0, 8):
			if (crc & 0x0001) > 0:
				crc = (crc >> 1) ^ pol
			else:
				crc = (crc >> 1)
	return (crc & 0xFFFF) + (crc >> 16)


def createPackage(identification, commandId, srcAddr, dstAddr, options):
	header = []

	# version and header size (IHL): 1 byte
	ver = 0x02 << 4
	ihl = ((len(options) + 3) // 4) + 5
	header.append(int(ver | ihl))

	# type of service: 1 byte (always zero)
	tos = 0x00
	header.append(int(tos))

	# total length: 2 bytes (in that case, same as IHL)
	tln = ihl
	header.append(int(ihl))

	# identification: 2 bytes
	idf = identification
	header.append(int(idf))

	# flags (0b000)  and fragment offset (always zero): 2 bytes
	flg = 0x00
	ffo = 0x00
	header.append(int((flg << 13) | ffo))

	# time to live (0x2A == 42d): 1 byte
	ttl = 0x2A
	header.append(int(ttl))

	# protocol: 2 bytes
	ptc = 0x00 | commandId
	header.append(int(ptc))

	# checksum: 2 bytes 
	chk = 0x00
	header.append(int(chk))

	# source address: 4 bytes
	src = struct.unpack('!I', srcAddr)
	src = src[0]
	header.append(int(src))

	# destination address: 4 bytes
	dst = struct.unpack('!I', dstAddr)
	dst = dst[0]
	header.append(int(dst))

	# options: variable size
	for i in options:
		header.append(int(ord(i)))

	# generates the checksum field
	chk = generateChecksum(header)

	# creates and fills package
	package = io.BytesIO()
	package.write(struct.pack('!B', (ver | ihl)))
	package.write(struct.pack('!B', tos))
	package.write(struct.pack('!H', tln))
	package.write(struct.pack('!H', idf))
	package.write(struct.pack('!H', ((flg << 13) | ffo)))
	package.write(struct.pack('!B', ttl))
	package.write(struct.pack('!B', ptc))
	package.write(struct.pack('!H', chk))
	package.write(struct.pack('!I', src))
	package.write(struct.pack('!I', dst))

	# adds the options to the package
	for i in options:
		package.write(struct.pack('!B', ord(i)))

	# add eof character and padding if needed		
	if ((len(package.getvalue()) % 4) != 0):
		package.write(struct.pack('!B', ord('\n')))
		while ((len(package.getvalue()) % 4) != 0):
			package.write(struct.pack('!B', 0))
	return package


def execute(maq, commands):
	identification = 0
	result = []

	# executes each command
	for cmd in commands:
		# verifies if argument contains dangerous arguments
		if (cmd[1].find("|") != -1):
			result.append("Error: '|' detected\n")
		elif (cmd[1].find(";") != -1):
			result.append("Error: ';' detected\n")
		elif (cmd[1].find(">") != -1):
			result.append("Error: '>' detected\n")

		# creates and initializes the connection
		client = socket(AF_INET, SOCK_STREAM)
		try:
			client.connect(("127.0.0.1", 9000 + maq))
		except error as e:
			result.append(str(e))
		
		# obtains the source and destination addresses
		srcAddr = inet_aton(gethostbyname(gethostname()))
		dstAddr = inet_aton("127.0.0.1")

		# creates the package
		numCmd = 0
		if (cmd[0] == "ps"):
			numCmd = 0
		elif (cmd[0] == "df"):
			numCmd = 1
		elif (cmd[0] == "finger"):
			numCmd = 2
		elif (cmd[0] == "uptime"):
			numCmd = 3
		identification = identification + 1	
		package = createPackage(identification, numCmd, srcAddr, dstAddr, cmd[1])
		package.seek(0)

		# sends the package
		try:
			client.send(package.read())
		except error as e:
			result.append(str(e))

		# obtains the response
		try:
			package = io.BytesIO(client.recv(65535))
		except error as e:
			result.append(str(e))

		# reads the package size ignoring header
		package.seek(0, 2)
		packageSize = package.tell() - 20

		# adds the content of the package to the result list
		package.seek(20)
		content = struct.unpack('s' * packageSize, package.read())
		result.append("".join(content))

		# closes connection		
		client.close()
	return result
