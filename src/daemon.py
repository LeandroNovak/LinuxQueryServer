#!/usr/bin/env python

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


def main():
	if ((len(sys.argv) == 3) && (sys.argv[1] == "--port")):

	else:
		print("Uso daemon.py --port PORT_NUMBER")
	lenOptions = 5
	print((lenOptions + 3) // 4)


if __name__ == "__main__":
	main()
