#!/usr/bin/env python3

from abc import abstractmethod
import RPi.GPIO as GPIO
import json
from coinbank import CoinBank 
import time

def readJSONPIN(path = "./pins.json"):
	with open(path, "r") as file:
		data = json.load(file)
		return data

class Pin() :
	id = 0
	pin = 0
	name = ""
	def __init__(self, id, pin, name, value = 0):
		self.id = id
		self.pin = pin # pin
		self.name = name # name 
		self.value = value # value
		pass

	def __str__(self):
		return f"{self.name}:({self.id}) - Pin({self.pin})"

class GPIOSystem():
	
	pins = []
	highest_pin : Pin = Pin(0, -1, "None") 

	def __init__(self) -> None:
		#JSON PIN SHEET (pins.json)
		self.pin_sheet = readJSONPIN()
		GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
		index = 0 # Index for pin
		for data in self.pin_sheet: # begin reading pin sheet 
			for name, pin in data.items(): 
					pin_obj = Pin(pin=pin, id=index, name=name) #create pin object
					# Add pin object to list
					self.addPin(pin_obj)
			index += 1
		self.start() # Start the GPIO System
		pass

	def addPin(self, pin: Pin):
		print(f"Adding Pin: {pin}")
		GPIO.setup(pin.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		self.pins.append(pin)
		pass

	def start(self):
		try:
			while True:
				for pin in self.pins:
					input_state = GPIO.input(pin.pin)
					if input_state == GPIO.LOW:
						print(f"Pin {pin} is LOW")
						self.highest_pin = self.maxPin(pin, self.highest_pin)
						if(pin.id == 0 and self.highest_pin.id > 0):
							self.highest_pin = self.pins[0]
							self.onPinReset(pin) #reset pin 
				time.sleep(0.5)
		except KeyboardInterrupt:
			# Clean up GPIO on keyboard interrupt
			print("Cleaning up GPIO")
			GPIO.cleanup()
		except Exception as e:
			print(f"Error: {e}")
			GPIO.cleanup()
		pass

	def maxPin(self, pin1: Pin , pin2 : Pin ) -> Pin :
		if pin2 is None:
			return pin1
		if pin1 is None:
			return pin2
		
		return pin1 if pin1.id > pin2.id else pin2

	def reset_highest_pin(self):
		self.highest_pin = self.pins[0] 
		pass

	def findPinData(self, pin: Pin):
		return self.pin_sheet[pin.id] 


	#abstract method that will be implemented in the child class
	@abstractmethod 
	def onPinReset(self, pin: Pin):
		highest_pin_copy = self.highest_pin
		self.reset_highest_pin()
		print(f"Resetting Highest Pin: {highest_pin_copy}")
		pass


class GPIOAPI(GPIOSystem):
	def __init__(self, coinbank: CoinBank) -> None:
		self.coinbank = coinbank		
		super().__init__()
		pass

	#override the onPinReset method, deposit x to the coinbank
	def onPinReset(self, pin: Pin):
		super().onPinReset(pin)
		self.coinbank.deposit(pin.value);
		print(f"{pin.name} - Balance: {self.coinbank.display()}")
		pass
