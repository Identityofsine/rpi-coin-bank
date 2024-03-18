#!/usr/bin/env python3

import RPi.GPIO as GPIO
import json
from coinbank import CoinBank 
import time

def readJSONPIN(path = "./pins.json"):
	with open(path, "r") as file:
		data = json.load(file)
		return data

class GPIOSystem():
	
	def __init__(self) -> None:
		pin_sheet = readJSONPIN()
		GPIO.setmode(GPIO.BCM)
		for pin in pin_sheet:
			print(f"Setting up pin {pin_sheet[pin]}")
			pin_number = int(pin_sheet[pin])
			#check if the pin_number is a number
			if not isinstance(pin_number, int):
				raise ValueError(f"Pin number {pin_number} is not a number")
			self.addPin(pin_number)
		self.start()
		pass

	def addPin(self, pin: int):
		GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		pass

	def start(self):
		try:
			while True:
				for pin in readJSONPIN():
					input_state = GPIO.input(pin)
					if input_state == GPIO.HIGH:
						print(f"Pin {pin} is HIGH")
					else:
						print(f"Pin {pin} is LOW")
					time.sleep(0.5)
		except KeyboardInterrupt:
			# Clean up GPIO on keyboard interrupt
			print("Cleaning up GPIO")
			GPIO.cleanup()
		except Exception as e:
			print(f"Error: {e}")
			GPIO.cleanup()
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
