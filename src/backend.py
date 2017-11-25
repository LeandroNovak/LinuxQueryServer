#!/usr/bin/env python
import struct
import io

def generateChecksum(data):
	data = list(data.getvalue())
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
	print("crc: " + str(crc))
	return crc

def createPackage(identification, commandId, srcAddr, dstAddr, options):
	package = io.BytesIO()
	ver = 0x02 << 4
	ihl = ((len(options) + 3) // 4) + 5
	package.write(struct.pack('!B', ver | ihl))
	tos = 0x00
	package.write(struct.pack('!B', tos))
	tln = ihl
	package.write(struct.pack('!H', tln))
	idf = identification
	package.write(struct.pack('!H', idf))
	flg = 0x00
	ffo = 0x00
	package.write(struct.pack('!H', (flg << 13) | ffo))
	ttl = 0x2A
	package.write(struct.pack('!B', ttl))
	ptc = 0x0000 | commandId
	package.write(struct.pack('!B', ptc))
	#chk = 0
	#package.write(struct.pack('!H', chk))
	src = srcAddr
	package.write(struct.pack('!I', src))
	dst = dstAddr
	package.write(struct.pack('!I', dst))
	chk = generateChecksum(package)
	opt = bytearray(options)
	
	print(len(package.getvalue()))
	return package


def execute(maq, commands):
	for cmd in commands:
		client = socket(AF_INET, SOCK_STREAM)
		client.connect(("127.0.0.1". 9000 + maq))
		srcAddr = inet_aton(gethostbyname(gethostbyname()))
		dstAddr = inet_aton("127.0.0.1")
		#package = createPackage()
		client.send(package.read())
		client.close()
	identificantion = 1
	

def main():
	options = "-r -s - t 1"
	print("lo: " + str(len(options)))
	createPackage(1, 2, 3, 4, options)
	

if __name__ == "__main__":
	main()
