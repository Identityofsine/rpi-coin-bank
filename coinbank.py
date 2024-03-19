

class CoinBank():
	
	# Variables (private)
	__balance = 0
	__id = 0


	# Constructor
	def __init__(self):
		self.__id = 0

	# Methods
	
	def deposit(self, amount) -> int:
		self.__balance += amount
		return self.__balance

	def withdraw(self, amount) -> int:
		if(amount > self.__balance):
			raise ValueError("Insufficient funds")
		self.__balance -= amount
		return self.__balance

	def display(self) -> int:
		return self.__balance
	

