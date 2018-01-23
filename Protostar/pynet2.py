import sys
import socket
import argparse
import struct


def main():
	
	# Make socket and connect
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((args.host, args.port))

	summ = 0
	for i in range(4):		
		data = sock.recv(4)
		num1 = struct.unpack("<I", data)[0]
		print("Num: ", num1)
		summ += int(num1)

	packed_sum = struct.pack("<I", summ)
	sock.send(packed_sum)

	data = sock.recv(1024)
	print(data.decode("utf-8"))


if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(description="Sumator")
	arg_parser.add_argument("host")
	arg_parser.add_argument("port", type=int)
	args = arg_parser.parse_args()

	main()