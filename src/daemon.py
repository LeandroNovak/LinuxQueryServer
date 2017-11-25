#!/usr/bin/env python

def generateChecksum(header):
	pol = 0x8421
	crc = 0
	return crc

def verifyChecksum(header, crc):
	return (generateChecksum(header) == crc)


def main():
	lenOptions = 5
	print((lenOptions + 3) // 4)


if __name__ == "__main__":
	main()
