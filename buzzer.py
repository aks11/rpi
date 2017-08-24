#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

BUZZER_PIN = 20

def init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BUZZER_PIN,GPIO.OUT)
	GPIO.output(BUZZER_PIN,GPIO.LOW)

def Beep():
	for count in range(0,1000):
		GPIO.output(BUZZER_PIN,GPIO.HIGH)
		time.sleep(0.000167)
		GPIO.output(BUZZER_PIN,GPIO.LOW)
		time.sleep(0.000167)

def main():

	init()

	print("\nInterfacing Buzzer(CHB-04F) with RPI3 & Python.")
	print("\nThis program runs indefinitely.\nTo quit, Press Ctrl+c...")
	
	while True:
		Beep()
		Beep()
		time.sleep(1)

if __name__ == "__main__":
	main()
	GPIO.close()