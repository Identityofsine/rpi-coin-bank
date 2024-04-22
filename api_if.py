import requests
import json

class API():
	def __init__(self, base_url=""):
		self.__base_url = base_url
		pass

	#push data to the server
	def updateCoinBase(self, coin = 0):
		response = self.post(self.__base_url, {"value": coin})
		return response

	@staticmethod
	def get(url = ""):
		try:
			response = requests.get(url)
			return response.json()
		except:
			return None
	
	@staticmethod
	def post(url = "", data = {}):
		try:
			response = requests.post(url, data)
			return response.json()
		except:
			return None

class Coinbank():
	def __init__(self, token = "", id = 0):
		self.__api = API("http://localhost:3000/")
		self.__token = token
		self.__id = id
		pass

	@staticmethod
	def loadInstance():
		file = open("coinbank.json", "r")
		if file is None:
			print("Error: file not found -- please create connect to the server first.")
			return None
		json_instance = json.load(file)
		return Coinbank(json_instance["token"], json_instance["id"])
		
	
