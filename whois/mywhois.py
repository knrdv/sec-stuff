import socket
import sys
from response_parsers import ResponseParser
import argparse

"""
Program which mimics WHOIS client. Currently supports only .com domain.
This is an exercuse student project.
"""

def parse_domain(domain):
	"""Extract top level domain from given address"""
	domain = domain.lower()
	domain_split = domain.split(".")
	if domain_split[0] == "www":
		domain_split = domain_split[1:]
	top_level_domain = ""
	if len(domain_split) > 2:
		top_level_domain = '.'.join(domain_split[-2:])
	else:
		top_level_domain = domain_split[-1]
	return top_level_domain	


def main():
	domain = args.address
	PORT = 43

	with open("./whois-servers.txt") as f:
		server_list = f.readlines()

	# Load servers
	server_map = {}
	for server in server_list:
		server = server.strip()
		server_list = server.split(" ")
		server_map[server_list[0]] = server_list[1]
	
	tld = parse_domain(domain)

	server = ""
	if tld not in server_map:
		print("[ERROR] No server for specified TLD")
		sys.exit()
	else:
		server = server_map[tld]
		print("[OK] Server for specified domain is: " + str(server))

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	request = domain + "\r\n"
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server, PORT))
	sock.send(request.encode("utf8"))
	response = sock.recv(4096).decode("utf8")
	sock.close()

	response_parser = ResponseParser(tld)
	domain_info = response_parser.parse(response)

	for k, v in domain_info.items():
		print(str(k) + " => " + str(v))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("address", help="Address fro lookup, example: youtube.com")
	args = parser.parse_args()
	main()