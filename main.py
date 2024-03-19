#!/usr/bin/env python3

import RPi.GPIO as GPIO
from coinbank import CoinBank 
from gpio import GPIOAPI, GPIOSystem
import time

coinbank = CoinBank()
x = GPIOAPI(coinbank)



