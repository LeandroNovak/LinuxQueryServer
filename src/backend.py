#!/usr/bin/env python

def generateChecksum(header, pol=0x8421):
	crc = 0
	return crc
	

def createPackage(identification, commandId, srcAddr, dstAddr, options):
	ver = 0x02
	ihl = ((len(options) + 3) // 4) + 5
	tos = 0x00
	idf = identification
	ffo = 0x00
	ttl = 0x2A
	ptc = 0x0000 | commandId
	chk = 0
	src = srcAddr
	dst = dstAddr
	

def execute(commands):
	identificantion = 1
	

def main():
	lenOptions = 5
	print((lenOptions + 3) // 4)


if __name__ == "__main__":
	main()
