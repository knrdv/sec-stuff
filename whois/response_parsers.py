import sys


class ResponseParser():
	""" Class for parsing incoming responses.

		Attributes:
			tld: top level domain, such as "com"

		Currently supports only "com" top level domains
	"""

	def __init__(self, tld="com"):
		self.tld = tld

	def parse(self, response):
		if self.tld == "com":
			return self.comParse(response)
		else:
			print("[ERROR] Current TLD not supported")
			sys.exit()

	def comParse(self, response):
		result = {}
		response = response.split("\n")
		for r in range(len(response)):
			response[r] = response[r].strip()
			if response[r].startswith(">"):
				response = response[:r]
				break
		for r in response:
			templist = r.split(":", 1)
			key = templist[0].lower()
			val = templist[1].strip()
			real_key = "_".join(key.split(" "))
			if real_key not in result:
				result[real_key] = [val]
			else:
				result[real_key].append(val)
		return result

