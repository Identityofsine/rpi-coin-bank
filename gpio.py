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
	def __init__(self, id, pin, name):
		self.id = id
		self.pin = pin
		self.name = name 
		pass

	def __str__(self):
		return f"{self.name}:({self.id}) - Pin({self.pin})"

class GPIOSystem():
	
	pins = []
	highest_pin : Pin = Pin(0, -1, "None") 

	def __init__(self) -> None:
		self.pin_sheet = readJSONPIN()
		GPIO.setmode(GPIO.BCM)
		index = 0
		for data in self.pin_sheet:
			for name, pin in data.items():
					pin_obj = Pin(pin=pin, id=index, name=name)
					self.pins.append(pin_obj)	
					self.addPin(pin_obj)
			index += 1
		self.start()
		pass

	def addPin(self, pin: Pin):
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
							#time.sleep(0.5)
					self.highest_pin = self.maxPin(pin, self.highest_pin)
					print(f"Highest Pin: {self.highest_pin}")
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


	@abstractmethod 
	def onPinReset(self, pin: int):
		pass


# Set GPIO mode to BCM
#pin = 2

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.output(pin, GPIO.HIGH)

#try:
#    while True:
#        # Read the state of pin 2
#        input_state = GPIO.input(pin)
        
#        # Check if the pin is high or low
#        if input_state == GPIO.HIGH:
#            print(f"Pin {pin} is HIGH")
#        else:
#            print(f"Pin {pin} is LOW")
        
#        # Wait for a short duration before reading again
#        time.sleep(0.5)

#except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
#    GPIO.cleanup()
